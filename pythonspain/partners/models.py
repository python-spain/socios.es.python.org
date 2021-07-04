import datetime
import re
from typing import TYPE_CHECKING, Dict
from functools import partial

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel
from options.models import Option

from pythonspain.core.models import BaseExport
from pythonspain.partners.constants import (
    ANNUAL,
    CHARGES,
    LATE,
    NOTICE_TYPES,
    PAYMENT_METHODS,
    WIRE_TRANSFER,
)
from pythonspain.partners.emails import (
    AnnualFeeReminder,
    LateFeeReminder,
    PartnerWelcomeEmail,
)
from pythonspain.partners.helpers import export_members, export_partners
from pythonspain.partners.managers import PartnerQuerySet
from pythonspain.partners.tasks import member_export_task, partner_export_task

if TYPE_CHECKING:
    from snitch.emails import TemplateEmailMessage


def partner_files_directory_path(subdir, instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return "partners/{instance.number}/{subdir}/{filename}"


class Partner(TimeStampedModel):
    """A partner is a person who is paying the partner fee."""

    number = models.CharField(
        _("number"), max_length=10, unique=True, db_index=True, blank=True
    )
    nif = models.CharField(_("NIF"), max_length=20, null=True, blank=True)
    name = models.CharField(_("name"), max_length=100)
    phone = models.CharField(_("phone"), max_length=20, null=True, blank=True)
    email = models.EmailField(_("email"), max_length=75)
    request_date = models.DateField(_("request date"), blank=True, null=True)
    approval_date = models.DateField(_("approval date"), blank=True, null=True)
    has_board_directors_charge = models.BooleanField(
        _("has board directors charge"), default=False
    )
    charge = models.CharField(
        _("charge"), max_length=16, choices=CHARGES, blank=True, null=True
    )
    is_founder = models.BooleanField(_("is founder"), default=False)
    is_active = models.BooleanField(_("is active"), default=True)
    comment = models.TextField(_("comment"), blank=True, null=True)
    bank_account = models.CharField(
        _("bank account"), max_length=30, blank=True, null=True
    )
    identity_doc = models.FileField(
        _("identity document"),
        upload_to=partial(partner_files_directory_path, "identity_doc"),
        blank=True, null=True
    )
    first_payment_doc = models.FileField(
        _("first payment document"),
        upload_to=partial(partner_files_directory_path, "first_payment_doc"),
        null=True, blank=True
    )
    is_rgpd_consent = models.BooleanField(_("is RGPD consent"), default=True)
    allow_notifications = models.BooleanField(_("allow sent notificacions"),
                                              default=True)

    objects = PartnerQuerySet.as_manager()

    class Meta:
        verbose_name = _("Partner")
        verbose_name_plural = _("Partners")
        ordering = ["-number"]

    def __str__(self):
        return self.name

    def get_short_name(self):
        """Gets the name of the partner."""
        return "".join(self.name.split(" ")[:1])

    def get_number(self):
        """Gets the partner number without the prefix and as an int."""
        return int(self.number.split("PYES-")[1])

    def clean(self):
        # Set number if is empty
        if not self.number:
            number = 1
            last = self.__class__.objects.order_by("number").last()
            if last:
                number += last.get_number()
            self.number = f"PYES-{number:04}"

        # Check number format
        if not re.match(r"PYES-[0-9]{4}", self.number):
            raise ValidationError({"number": _("The number format is not correct.")})

        # Remove spaces from back account
        if self.bank_account:
            self.bank_account = self.bank_account.replace(" ", "")

    def send_welcome(self):
        """Sends the welcome email."""
        email = PartnerWelcomeEmail(to=self.email, context={"partner": self})
        email.send()

    def create_and_send_notice(self, kind: str) -> "Notice":
        """Creates a notice for this partner."""
        notice = Notice.objects.create(partner=self, kind=kind)
        notice.send()
        return notice

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        # Automatic welcome emails
        activate_welcome_emails = bool(
            Option.objects.get_value("activate_welcome_emails", default=0)
        )
        if self._state.adding and activate_welcome_emails:
            self.send_welcome()


class Fee(TimeStampedModel):
    """Annotations for paid fees from the partners."""

    partner = models.ForeignKey(
        "partners.Partner",
        related_name="fees",
        on_delete=models.CASCADE,
        verbose_name=_("partner"),
    )
    date = models.DateField(_("date"), null=True, blank=True)
    payment_method = models.CharField(
        _("payment method"),
        max_length=16,
        choices=PAYMENT_METHODS,
        default=WIRE_TRANSFER,
    )
    amount = models.DecimalField(
        _("amount"), max_digits=5, decimal_places=2, default="30.00"
    )

    class Meta:
        verbose_name = _("Fee")
        verbose_name_plural = _("Fees")
        ordering = ["-date"]

    def __str__(self):
        return f"{str(self.partner)}: {self.amount} ({self.date})"


class Notice(TimeStampedModel):
    """A notice sent to a partner to remember the fee."""

    kind = models.CharField(
        _("kind"), choices=NOTICE_TYPES, max_length=16, default=LATE
    )
    partner = models.ForeignKey(
        "partners.Partner",
        related_name="notices",
        on_delete=models.CASCADE,
        verbose_name=_("partner"),
    )
    date = models.DateField(
        _("date"), null=True, blank=True, default=datetime.datetime.today
    )
    comment = models.TextField(_("comment"), null=True, blank=True)

    class Meta:
        verbose_name = _("Notice")
        verbose_name_plural = _("Notices")

    def __str__(self):
        return str(self.date)

    def _notice_email_context(self) -> Dict:
        last_fee = self.partner.fees.order_by("-date").first()
        return {"partner": self.partner, "last_fee": last_fee}

    def _email_class(self) -> "TemplateEmailMessage":
        email_classes = {LATE: LateFeeReminder, ANNUAL: AnnualFeeReminder}
        return email_classes.get(self.kind)

    def send(self):
        """Sends the reminder fee email."""
        treasury_email = Option.objects.get_value(
            "treasury_email", default="tesoreria@es.python.org"
        )
        email = self._email_class()(
            to=self.partner.email,
            from_email=f"Tesorería Python España <{treasury_email}>",
            reply_to=treasury_email,
            context=self._notice_email_context(),
        )
        email.send()


class Member(TimeStampedModel):
    """A non-paid member."""

    name = models.CharField(_("name"), max_length=100)
    email = models.EmailField(_("email"), max_length=75, null=True)

    class Meta:
        verbose_name = _("Member")
        verbose_name_plural = _("Members")
        ordering = ["-created"]

    def __str__(self):
        return self.name


class PartnerExport(BaseExport):
    FILE_NAME = "partners"

    class Meta:
        verbose_name = _("Partners export")
        verbose_name_plural = _("Partners exports")
        ordering = ["-created"]

    def get_queryset(self):
        """Gets the QuerySet to export."""
        return Partner.objects.all().annotate_last_fee_date()

    def exporter(self):
        """Gets the export helper function that does the export."""
        return export_partners

    def exporter_task(self):
        """Gets the async task that does the exporter."""
        return partner_export_task


class MemberExport(BaseExport):
    FILE_NAME = "members"

    class Meta:
        verbose_name = _("Members export")
        verbose_name_plural = _("Members exports")
        ordering = ["-created"]

    def get_queryset(self):
        """Gets the QuerySet to export."""
        return Member.objects.all()

    def exporter(self):
        """Gets the export helper function that does the export."""
        return export_members

    def exporter_task(self):
        """Gets the async task that does the exporter."""
        return member_export_task

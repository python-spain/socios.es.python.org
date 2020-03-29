import re
import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel

from pythonspain.partners.constants import CHARGES, PAYMENT_METHODS, WIRE_TRANSFER
from pythonspain.partners.managers import PartnerQuerySet
from django.core.exceptions import ValidationError


class Partner(TimeStampedModel):
    """A partner is a person who is paying the partner fee."""

    number = models.CharField(_("number"), max_length=10, unique=True, db_index=True)
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
    comment = models.TextField(_("comment"), null=True, blank=True)
    bank_account = models.CharField(
        _("bank account"), max_length=30, blank=True, null=True
    )

    objects = PartnerQuerySet.as_manager()

    class Meta:
        verbose_name = _("Partner")
        verbose_name_plural = _("Partners")
        ordering = ["-number"]

    def __str__(self):
        return self.name

    def clean(self):
        # Check number format
        if not re.match(r"PYES-[0-9]{4}", self.number):
            raise ValidationError({"number": _("The number format is not correct.")})
        # Remove spaces from back account
        if self.bank_account:
            self.bank_account = self.bank_account.replace(" ", "")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


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
    """A notice sent to a partner."""

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


class Member(TimeStampedModel):
    """A non-paid member."""

    name = models.CharField(_("name"), max_length=100)

    class Meta:
        verbose_name = _("Member")
        verbose_name_plural = _("Members")
        ordering = ["-created"]

    def __str__(self):
        return self.name

from django.utils.translation import gettext_lazy as _
from snitch.emails import TemplateEmailMessage


class PartnerWelcomeEmail(TemplateEmailMessage):
    """Email notification sent when a new partner is created."""

    default_template_name = "emails/welcome.html"
    default_subject = _("Approval as partner in Python Spain")


class LateFeeReminder(TemplateEmailMessage):
    """Email for partners with reminder fee."""

    default_template_name = "emails/reminder_late.html"
    default_subject = _("Late fee reminder")


class AnnualFeeReminder(TemplateEmailMessage):
    """Email for partners with reminder fee."""

    default_template_name = "emails/reminder_annual.html"
    default_subject = _("Annual fee reminder")

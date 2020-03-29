from django.utils.translation import gettext_lazy as _

from snitch.emails import TemplateEmailMessage


class VerificationEmail(TemplateEmailMessage):
    """Email notification when when an user is register, to verify his email."""

    default_template_name = "emails/verification.html"
    default_subject = _("Verify your email")


class RestorePasswordEmail(TemplateEmailMessage):
    """Email notification when when an user request a restore password code."""

    default_template_name = "emails/restore_password.html"
    default_subject = _("Restore your password")

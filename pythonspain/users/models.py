import hashlib
import random
import time

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from pythonspain.users.emails import RestorePasswordEmail, VerificationEmail
from pythonspain.users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """Custom User model."""

    email = models.EmailField(
        _("email"),
        unique=True,
        error_messages={"unique": _("There is another user with this email")},
    )

    first_name = models.CharField(_("first name"), max_length=30, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    # Restore password
    restore_password_code = models.CharField(
        max_length=256, unique=True, null=True, blank=True
    )
    restore_password_code_requested_at = models.DateTimeField(null=True, blank=True)

    # Email verification
    is_email_verified = models.BooleanField(
        _("verified"),
        default=False,
        help_text=_("Designates if the user has the email verified."),
    )
    verification_code = models.CharField(
        max_length=256, unique=True, null=True, blank=True
    )

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ("date_joined",)

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def generate_random_code(self):
        """Generates a restore password code."""
        return hashlib.sha256(
            ("{}-{}-{}".format(self.email, time.time(), random.randint(0, 10))).encode(
                "utf-8"
            )
        ).hexdigest()

    def send_restore_code(self):
        """Sends an email with the link to restore the password."""
        self.restore_password_code = self.generate_random_code()
        self.restore_password_code_requested_at = timezone.now()
        self.save()
        email = RestorePasswordEmail(to=self.email, context={"user": self})
        email.send()

    def reset_verification(self, commit=False):
        """Resets the email verification."""
        self.is_email_verified = False
        self.verification_code = self.generate_random_code()
        if commit:
            self.save()

    def send_verification(self):
        """Send the validation email, to validate the user's email."""
        assert self.pk is not None
        assert not self.is_email_verified
        assert self.verification_code is not None

        email = VerificationEmail(to=self.email, context={"user": self})
        email.send()

    def verify(self):
        """Verifies this email user."""
        self.is_email_verified = True
        self.verification_code = None
        self.save()

    def save(self, *args, **kwargs):
        is_insert = self._state.adding
        # Checks change of email
        if not is_insert:
            previous_user = User.objects.get(pk=self.pk)
            if previous_user.email != self.email:
                self.is_email_verified = False
                self.verification_code = None
        # Creates verification code if it doesn't exists
        if not self.is_email_verified and (
            self.verification_code is None or self.verification_code.strip() == ""
        ):
            self.verification_code = self.generate_random_code()
        result = super().save(*args, **kwargs)
        # For every inserts, sends a verification email (excepts superusers)
        if is_insert and not self.is_email_verified and not self.is_superuser:
            self.send_verification()
        return result

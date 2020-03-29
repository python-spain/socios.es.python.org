from django import forms
from django.contrib.auth import get_user_model, forms as admin_forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class UserChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(admin_forms.UserCreationForm):

    error_message = admin_forms.UserCreationForm.error_messages.update(
        {"duplicate_email": _("This email has already been taken.")}
    )

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        fields = ("email",)

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise ValidationError(self.error_messages["duplicate_email"])


class RestorePasswordForm(forms.Form):
    """Form to restore password."""

    password = forms.fields.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "input", "placeholder": _("New Password")}
        ),
        error_messages={"required": _("The password is required")},
    )
    repeat_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "input", "placeholder": _("Repeat Password")}
        )
    )
    restore_password_code = forms.fields.CharField(
        widget=forms.HiddenInput(), required=True
    )

    def clean_restore_password_code(self):
        restore_password_code = self.cleaned_data.get("restore_password_code")
        if not User.objects.filter(
            restore_password_code=restore_password_code
        ).exists():
            raise forms.ValidationError(_("Restore code doesn't exists"))
        return restore_password_code

    def clean_repeat_password(self):
        password = self.cleaned_data.get("password")
        repeat_password = self.cleaned_data.get("repeat_password")
        if password and repeat_password and password != repeat_password:
            raise forms.ValidationError(_("Passwords are not the same"))
        return repeat_password

    def save(self):
        restore_password_code = self.cleaned_data.get("restore_password_code")
        password = self.cleaned_data.get("password")
        user = User.objects.get(restore_password_code=restore_password_code)
        user.set_password(password)
        user.save()
        return user

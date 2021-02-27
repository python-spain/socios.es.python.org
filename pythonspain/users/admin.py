from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from pythonspain.users.forms import UserChangeForm, UserCreationForm

User = get_user_model()


def send_restore_code_action(modeladmin, request, queryset):
    for user in queryset:
        user.send_restore_code()
    modeladmin.message_user(request, _("Restore password codes sent!"))


send_restore_code_action.short_description = _(  # type: ignore
    "Send restore password code"
)


def send_verification_action(modeladmin, request, queryset):
    for user in queryset:
        user.reset_verification()
        user.send_verification()
    modeladmin.message_user(request, _("Email verification sent!"))


send_verification_action.short_description = _(  # type: ignore
    "Send email verification"
)


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
        (
            _("Restore password"),
            {"fields": ("restore_password_code", "restore_password_code_requested_at")},
        ),
        (
            _("Email verification"),
            {"fields": ("is_email_verified", "verification_code")},
        ),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),
    )
    ordering = ("date_joined",)
    list_display = ["email", "first_name", "last_name", "is_superuser", "date_joined"]
    search_fields = ["first_name", "last_name", "email"]
    actions = [send_restore_code_action, send_verification_action]

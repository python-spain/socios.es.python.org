from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from django.utils.translation import gettext_lazy as _
from django.views import View

from pythonspain.users.forms import RestorePasswordForm, User


class RestorePasswordView(View):
    """View to handle the restore of the password."""

    template_name: str = "users/restore_password.html"
    form_class = RestorePasswordForm

    def get(self, request, restore_password_code):
        form = self.form_class(initial={"restore_password_code": restore_password_code})
        data = {"form": form, "restore_password_code": restore_password_code}
        return render(request, self.template_name, data)

    def post(self, request, restore_password_code):
        form = self.form_class(request.POST)
        data = {"form": form, "restore_password_code": restore_password_code}
        if form.is_valid():
            form.save()
            messages.success(request, _("Password updated!"))
        return render(request, self.template_name, data)


class VerifiedView(View):
    """View to handle verification of users."""

    template_name: str = "users/verified.html"

    def get(self, request, verification_code):
        user = get_object_or_404(User, verification_code=verification_code)
        user.verify()
        messages.success(request, _("User verified!"))
        return render(request, self.template_name)

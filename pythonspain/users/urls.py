from django.urls import path

from pythonspain.users.views import RestorePasswordView, VerifiedView

app_name = "users"
urlpatterns = [
    path("verified/<str:verification_code>/", VerifiedView.as_view(), name="verified"),
    path(
        "restore-password/<str:restore_password_code>/",
        RestorePasswordView.as_view(),
        name="restore-password",
    ),
]

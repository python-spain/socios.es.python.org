from django.contrib.auth import get_user_model

User = get_user_model()


def restore_password(restore_password_code: str, password: str):
    """Restore the password of the user with the restore_password_code code."""
    user = User.objects.get(restore_password_code=restore_password_code)
    user.set_password(password)
    user.save()


def verify_email(verification_code: str):
    user = User.objects.get(verification_code=verification_code)
    user.verify()
    user.save()

def restore_password(restore_password_code, password):
    """Restore the password of the user with the restore_password_code code."""
    from pythonspain.users.models import User

    user = User.objects.get(restore_password_code=restore_password_code)
    user.set_password(password)
    user.save()


def verify_email(verification_code):
    from pythonspain.users.models import User

    user = User.objects.get(verification_code=verification_code)
    user.verify()
    user.save()

from django.urls import reverse
from test_plus import TestCase

from pythonspain.users.tests.factories import UserFactory


class RestorePasswordViewTest(TestCase):
    user_factory = UserFactory

    def setUp(self):
        self.user = self.make_user()

    def test_get_restore_password_view(self):
        self.user.send_restore_code()
        with self.login(self.user):
            self.get(
                reverse(
                    "users:restore-password",
                    kwargs={"restore_password_code": self.user.restore_password_code},
                )
            )
            self.response_200()


class VerifiedViewTest(TestCase):
    user_factory = UserFactory

    def setUp(self):
        self.user = self.make_user()

    def test_verified_user(self):
        user = UserFactory()
        user.is_email_verified = False
        user.save()
        self.assertIsNotNone(user.verification_code)
        self.get(
            reverse(
                "users:verified", kwargs={"verification_code": user.verification_code}
            )
        )
        user.refresh_from_db()
        self.assertTrue(user.is_email_verified)

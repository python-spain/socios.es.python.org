from test_plus import TestCase

from pythonspain.users.forms import RestorePasswordForm
from pythonspain.users.tests.factories import UserFactory


class RestorePasswordFormTest(TestCase):
    user_factory = UserFactory

    def setUp(self):
        self.user = self.make_user()

    def test_restore_password_form(self):
        self.user.send_restore_code()
        data = {
            "repeat_password": "potato123",
            "password": "potato123",
            "restore_password_code": self.user.restore_password_code,
        }
        form = RestorePasswordForm(data)
        self.assertTrue(form.is_valid())
        form.save()
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(data["password"]))

    def test_restore_password_form_not_valid(self):
        self.user.send_restore_code()
        data = {
            "repeat_password": "potato123",
            "password": "potato321",
            "restore_password_code": self.user.restore_password_code,
        }
        form = RestorePasswordForm(data)
        self.assertFalse(form.is_valid())

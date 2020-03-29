from test_plus import TestCase

from pythonspain.banks.helpers import import_consignments
from pythonspain.partners.tests.factories import PartnerFactory
from pythonspain.users.tests.factories import UserFactory


class HelpersTestCase(TestCase):
    user_factory = UserFactory

    def test_import_consignments(self):
        PartnerFactory.create_batch(size=5)
        with open("pythonspain/banks/tests/consignments.xls", "rb") as file:
            fees = import_consignments(file)
        self.assertEqual(5, fees.count())

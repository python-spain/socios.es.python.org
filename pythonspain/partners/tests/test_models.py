import datetime

from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from test_plus import TestCase

from pythonspain.partners.models import Partner
from pythonspain.partners.tests.factories import FeeFactory, PartnerFactory
from pythonspain.users.tests.factories import UserFactory


class PartnerTestCase(TestCase):
    user_factory = UserFactory

    def test_incorrect_number(self):
        try:
            PartnerFactory(number="PY-001")
            exception = False
        except ValidationError:
            exception = True
        self.assertTrue(exception)

    def test_correct_number(self):
        try:
            PartnerFactory(number="PYES-0001")
            exception = False
        except ValidationError:
            exception = True
        self.assertFalse(exception)

    def test_annotate_last_fee_date(self):
        partners = PartnerFactory.create_batch(size=10)
        for partner in partners:
            fee = FeeFactory(partner=partner, date=datetime.datetime.today())
            FeeFactory(partner=partner, date=fee.date - relativedelta(years=1))
        partners = Partner.objects.annotate_last_fee_date()
        self.assertTrue(hasattr(partners[0], "last_fee_date"))

    def test_direct_debit(self):
        no_direct_debit_partners = PartnerFactory.create_batch(size=3)
        direct_debit_partners = PartnerFactory.create_batch(size=5, bank_account="ES00")

        self.assertEqual(
            len(direct_debit_partners), Partner.objects.direct_debit().count()
        )
        self.assertEqual(
            len(no_direct_debit_partners), Partner.objects.direct_debit(False).count()
        )

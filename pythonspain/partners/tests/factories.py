import factory

from pythonspain.partners.models import Partner, Fee


class PartnerFactory(factory.DjangoModelFactory):
    number = factory.Sequence(lambda n: f"PYES-{n + 1:04}")
    name = factory.Faker("first_name")
    email = factory.Faker("email")

    class Meta:
        model = Partner


class FeeFactory(factory.DjangoModelFactory):
    partner = factory.SubFactory(PartnerFactory)

    class Meta:
        model = Fee

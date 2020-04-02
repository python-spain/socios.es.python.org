import factory

from pythonspain.partners.models import (
    Fee,
    Member,
    MemberExport,
    Partner,
    PartnerExport,
)


class PartnerFactory(factory.DjangoModelFactory):
    number = factory.Sequence(lambda n: f"PYES-{n + 1:04}")
    name = factory.Faker("first_name")
    email = factory.Faker("email")

    class Meta:
        model = Partner


class MemberFactory(factory.DjangoModelFactory):
    name = factory.Faker("first_name")
    email = factory.Faker("email")

    class Meta:
        model = Member


class FeeFactory(factory.DjangoModelFactory):
    partner = factory.SubFactory(PartnerFactory)

    class Meta:
        model = Fee


class PartnerExportFactory(factory.DjangoModelFactory):
    class Meta:
        model = PartnerExport


class MemberExportFactory(factory.DjangoModelFactory):
    class Meta:
        model = MemberExport

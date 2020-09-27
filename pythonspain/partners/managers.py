from django.apps import apps
from django.db import models
from django.db.models import OuterRef, Subquery
from django.utils import timezone


class PartnerQuerySet(models.QuerySet):
    def active(self):
        """Get active partners."""
        return self.filter(is_active=True)

    def direct_debit(self, value=True):
        """Filters partners with direct debit or not."""
        return self.filter(bank_account__isnull=not value)

    def annotate_last_fee_date(self):
        """Adds to the queryset the last date of a paid fee."""
        Fee = apps.get_model("partners.Fee")
        fees = Fee.objects.filter(partner=OuterRef("pk")).order_by("-date")
        return self.annotate(last_fee_date=Subquery(fees.values("date")[:1]))

    def delayed_fee(self):
        """Gets the partners with delayed fee."""
        today = timezone.now().date()
        return (
            self.active()
            .annotate_last_fee_date()
            .filter(last_fee_date__year__lt=today.year)
        )

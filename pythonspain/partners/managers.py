from django.db import models
from django.db.models import OuterRef, Subquery


class PartnerQuerySet(models.QuerySet):
    def direct_debit(self, value=True):
        """Filters partners with direct debit or not."""
        return self.filter(bank_account__isnull=not value)

    def annotate_last_fee_date(self):
        """Adds to the queryset the last date of a paid fee."""
        from pythonspain.partners.models import Fee

        fees = Fee.objects.filter(partner=OuterRef("pk")).order_by("-date")
        return self.annotate(last_fee_date=Subquery(fees.values("date")[:1]))

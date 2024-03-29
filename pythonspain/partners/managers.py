import datetime
from typing import Optional

from django.apps import apps
from django.db import models
from django.db.models import Count, F, OuterRef, Q, Subquery
from django.utils import timezone

from pythonspain.partners.constants import DIRECT_DEBIT


class PartnerQuerySet(models.QuerySet):
    def active(self) -> "PartnerQuerySet":
        """Get active partners."""
        return self.filter(is_active=True)

    def annotate_direct_debit_fees(self) -> "PartnerQuerySet":
        """Annotates the total of fees paid with direct debit."""
        return self.annotate(
            direct_debit_fees_count=Count(
                "fees", filter=Q(fees__payment_method=DIRECT_DEBIT)
            )
        )

    def direct_debit(self, value: bool = True) -> "PartnerQuerySet":
        """Filters partners with direct debit or not."""
        return self.filter(bank_account__isnull=not value)

    def first_direct_debit_fee(self) -> "PartnerQuerySet":
        """Gets the partners that has to pay the first direct debit fee."""
        return (
            self.annotate_direct_debit_fees()
            .filter(direct_debit_fees_count=0)
            .direct_debit()
            .active()
        )

    def renew_direct_debit_fee(self) -> "PartnerQuerySet":
        """Gets the partners that has to renew de fee using direct debit."""
        return (
            self.active()
            .annotate_direct_debit_fees()
            .filter(direct_debit_fees_count__gt=0)
            .direct_debit()
        )

    def pending_wire_transfer_fee(self) -> "PartnerQuerySet":
        """Gets the partners that has to pay the fee using wire transfer."""
        return self.active().delayed_fee().direct_debit(False)

    def annotate_last_fee_date(self) -> "PartnerQuerySet":
        """Adds to the queryset the last date of a paid fee."""
        Fee = apps.get_model("partners.Fee")
        fees = Fee.objects.filter(partner=OuterRef("pk")).order_by("-date")
        return self.annotate(last_fee_date=Subquery(fees.values("date")[:1]))

    def annotate_since_last_fee(
        self, date: Optional["datetime.date"] = None
    ) -> "PartnerQuerySet":
        date = timezone.now().date() if not date else date
        return self.annotate_last_fee_date().annotate(
            since_last_fee=date - F("last_fee_date")
        )

    def delayed_fee(self, date: Optional["datetime.date"] = None) -> "PartnerQuerySet":
        """Gets the partners with delayed fee."""
        date = timezone.now().date() if not date else date
        return (
            self.active()
            .annotate_since_last_fee(date=date)
            .filter(
                Q(since_last_fee__gte=datetime.timedelta(days=365))
                | Q(last_fee_date__isnull=True)
            )
        )

    def right_to_vote(self) -> "PartnerQuerySet":
        """Get the list of partners that has right to vote, that is: is active and has
        the fee up tp date, or is founder.
        """
        return (
            self.active()
            .annotate_since_last_fee()
            .filter(
                Q(is_founder=True) | Q(since_last_fee__lt=datetime.timedelta(days=365))
            )
        )

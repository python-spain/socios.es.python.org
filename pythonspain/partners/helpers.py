from typing import TYPE_CHECKING

from pythonspain.core.helpers import basic_exporter

if TYPE_CHECKING:
    from io import StringIO

    from pythonspain.partners.managers import PartnerQuerySet


def export_partners(queryset: "PartnerQuerySet", output: "StringIO") -> int:
    fieldnames = [
        "number",
        "nif",
        "name",
        "phone",
        "email",
        "request_date",
        "approval_date",
        "has_board_directors_charge",
        "charge",
        "is_founder",
        "is_active",
        "comment",
        "last_fee_date",
    ]
    return basic_exporter(queryset.order_by("-number"), output, fieldnames)


def export_members(queryset, output):
    fieldnames = ["name", "email", "created"]
    return basic_exporter(queryset.order_by("-created"), output, fieldnames)

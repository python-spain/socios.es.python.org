import csv
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from io import StringIO

    from django.db import models


def basic_exporter(
    queryset: "models.QuerySet", output: "StringIO", fieldnames: List
) -> int:
    writer = csv.DictWriter(output, fieldnames=fieldnames, delimiter=",")
    writer.writeheader()
    items = 0
    for model in queryset.iterator():
        row = dict()
        for field_name in fieldnames:
            row[field_name] = getattr(model, field_name)
        writer.writerow(row)
        items += 1
    return items

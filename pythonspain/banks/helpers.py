import datetime
from typing import TYPE_CHECKING

import xlrd

from pythonspain.partners.constants import DIRECT_DEBIT
from pythonspain.partners.models import Fee, Partner

if TYPE_CHECKING:
    from io import StringIO


def import_consignments(source: "StringIO"):
    """Helper function to handle the import of consignments from the bank. Returns a
    QuerySet of fees.
    """
    workbook = xlrd.open_workbook(file_contents=source.read())
    sheet = workbook.sheet_by_index(0)
    date = datetime.datetime.strptime(
        sheet.cell(1, 4).value, "%d/%m/%Y %H:%M:%S"
    ).date()
    fees_pks = []
    for row in range(sheet.nrows)[14:]:
        reference = sheet.cell(row, 0).value
        amount = float(sheet.cell(row, 5).value)
        try:
            partner = Partner.objects.get(number=reference)
            if not Fee.objects.filter(partner=partner, date=date).exists():
                fee = Fee(partner=partner, date=date, payment_method=DIRECT_DEBIT)
                fee.save()
                fees_pks.append(fee.pk)
        except Partner.DoesNotExist:
            pass
    return Fee.objects.filter(pk__in=fees_pks)

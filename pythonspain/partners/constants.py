from django.utils.translation import gettext_lazy as _

PRESIDENT, VICE_PRESIDENT, SECRETARY, TREASURER, VOCAL = (
    "president",
    "vicepresident",
    "secretary",
    "treasurer",
    "vocal",
)

CHARGES = (
    (PRESIDENT, _("President")),
    (VICE_PRESIDENT, _("Vice president")),
    (SECRETARY, _("Secretary")),
    (TREASURER, _("Treasurer")),
    (VOCAL, _("Vocal")),
)

WIRE_TRANSFER, DIRECT_DEBIT = "wire_transfer", "direct_debit"

PAYMENT_METHODS = (
    (WIRE_TRANSFER, _("Wire transfer")),
    (DIRECT_DEBIT, _("Direct debit")),
)

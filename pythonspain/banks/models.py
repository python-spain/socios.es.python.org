from typing import Callable

from django.utils.translation import gettext_lazy as _

from pythonspain.banks.helpers import import_consignments
from pythonspain.banks.tasks import import_consignments_task
from pythonspain.core.models import BaseImport


class ConsignmentImport(BaseImport):
    """Model to handle import of consignments."""

    class Meta:
        verbose_name = _("Consignment import")
        verbose_name_plural = _("Consignment imports")
        ordering = ["-created"]

    def importer(self) -> Callable:
        """Gets the helper function to handle import."""
        return import_consignments

    def importer_task(self) -> Callable:
        """Gets the task to launch import."""
        return import_consignments_task

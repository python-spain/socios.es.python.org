from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from pythonspain.banks.models import ConsignmentImport


def import_action(modeladmin, request, queryset):
    """Admin action to launch the import process."""
    for import_model in queryset:
        import_model.import_data(async_process=True)
    modeladmin.message_user(request, _("Launched import consignments tasks..."))


import_action.short_description = _("Import consignments")  # type: ignore


@admin.register(ConsignmentImport)
class ConsignmentImportAdmin(admin.ModelAdmin):
    list_display = ["id", "data", "status", "items", "created"]
    actions = [import_action]

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from pythonspain.partners.models import Fee, Member, Notice, Partner


@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ["id", "partner", "payment_method", "amount", "date"]
    list_filter = ["payment_method"]
    search_fields = [
        "partner__number",
        "partner__name",
        "partner__nif",
        "partner__email",
    ]
    autocomplete_fields = ["partner"]


class FeeInline(admin.TabularInline):
    model = Fee
    extra = 0


class NoticeInline(admin.TabularInline):
    model = Notice
    extra = 0


class DirectDebitListFilter(admin.SimpleListFilter):
    title = _("has direct debit")
    parameter_name = "direct_debit"

    def lookups(self, request, model_admin):
        return ((True, _("Yes")), (False, _("No")))

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.direct_debit(self.value())
        return queryset


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = [
        "number",
        "name",
        "request_date",
        "charge",
        "is_founder",
        "is_active",
        "last_fee_date",
    ]
    list_filter = [
        "is_active",
        "is_founder",
        "has_board_directors_charge",
        DirectDebitListFilter,
    ]
    search_fields = ["number", "name", "nif", "email"]
    inlines = [FeeInline, NoticeInline]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate_last_fee_date()

    def last_fee_date(self, instance):
        return instance.last_fee_date

    last_fee_date.short_description = _("last fee date")
    last_fee_date.admin_order_field = "last_fee_date"


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "created"]
    search_fields = ["name"]
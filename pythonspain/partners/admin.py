from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from pythonspain.partners.constants import ANNUAL, LATE
from pythonspain.partners.models import (
    Fee,
    Member,
    MemberExport,
    Notice,
    Partner,
    PartnerExport,
)


def send_late_fee_reminder_email_action(modeladmin, request, queryset):
    for partner in queryset.delayed_fee():
        partner.create_and_send_notice(kind=LATE)
    modeladmin.message_user(request, _("Late fee reminder sent!"))


send_late_fee_reminder_email_action.short_description = _("Send delayed fee reminder email")  # type: ignore


def send_annual_fee_reminder_action(modeladmin, request, queryset):
    for partner in queryset.pending_wire_transfer_fee():
        partner.create_and_send_notice(kind=ANNUAL)
    modeladmin.message_user(request, _("Annual reminder sent!"))


send_annual_fee_reminder_action.short_description = _("Send annual fee reminder email")  # type: ignore


def send_welcome_action(modeladmin, request, queryset):
    for partner in queryset:
        partner.send_welcome()
    modeladmin.message_user(request, _("Welcome email sent!"))


send_welcome_action.short_description = _("Send welcome email")  # type: ignore


def export_action(modeladmin, request, queryset):
    """Admin action to launch the export process."""
    for import_model in queryset:
        import_model.export_data(async_process=True)
    modeladmin.message_user(request, _("Launched export tasks..."))


export_action.short_description = _("Launch exports")  # type: ignore


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
            return queryset.direct_debit(self.value() == "True")
        return queryset


class LastFeeYearListFilter(admin.SimpleListFilter):
    title = _("last fee year")
    parameter_name = "last_fee_year"

    def lookups(self, request, model_admin):
        years = set(
            [
                date.year
                for date in model_admin.model.objects.active()
                .annotate_last_fee_date()
                .values_list("last_fee_date", flat=True)
                if date
            ]
        )
        return [(year, f"{year}") for year in sorted(years)]

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.annotate_last_fee_date().filter(
                last_fee_date__year=self.value()
            )
        return queryset


class HasRightToVoteListFilter(admin.SimpleListFilter):
    title = _("has right to vote")
    parameter_name = "has_right_to_vote"

    def lookups(self, request, model_admin):
        return [(True, _("Yes")), (False, _("No"))]

    def queryset(self, request, queryset):
        if self.value() is not None:
            if self.value() == "True":
                return queryset.right_to_vote()
            return queryset.exclude(
                pk__in=queryset.right_to_vote().values_list("pk", flat=True)
            )
        return queryset


class HasDelayedFeeListFilter(admin.SimpleListFilter):
    title = _("has delayed fee")
    parameter_name = "has_delayed_fee"

    def lookups(self, request, model_admin):
        return [(True, _("Yes")), (False, _("No"))]

    def queryset(self, request, queryset):
        if self.value() is not None:
            if self.value() == "True":
                return queryset.delayed_fee()
            return queryset.exclude(
                pk__in=queryset.delayed_fee().values_list("pk", flat=True)
            )
        return queryset


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    readonly_fields = ("number",)
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
        LastFeeYearListFilter,
        HasDelayedFeeListFilter,
        HasRightToVoteListFilter,
    ]
    search_fields = ["number", "name", "nif", "email"]
    inlines = [FeeInline, NoticeInline]
    actions = [
        send_welcome_action,
        send_annual_fee_reminder_action,
        send_late_fee_reminder_email_action,
    ]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate_last_fee_date()

    def last_fee_date(self, instance):
        return instance.last_fee_date

    last_fee_date.short_description = _("last fee date")  # type: ignore
    last_fee_date.admin_order_field = "last_fee_date"  # type: ignore


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "created"]
    search_fields = ["name"]


@admin.register(PartnerExport)
class PartnerExportAdmin(admin.ModelAdmin):
    list_display = ["id", "data", "status", "items", "created"]
    actions = [export_action]


@admin.register(MemberExport)
class MemberExportAdmin(admin.ModelAdmin):
    list_display = ["id", "data", "status", "items", "created"]
    actions = [export_action]

"""质量模块后台配置。"""

from django.contrib import admin
from django.utils.html import format_html

from apps.quality.models import DefectRecord, Inspection


class DefectRecordInline(admin.TabularInline):
    model = DefectRecord
    extra = 0
    fields = ("defect_type", "quantity", "cause", "action")


@admin.register(Inspection)
class InspectionAdmin(admin.ModelAdmin):
    list_display = (
        "batch_no",
        "work_order",
        "sample_qty",
        "defect_qty",
        "defect_rate_display",
        "result",
        "inspector",
        "inspected_at",
    )
    list_filter = ("result", "inspected_at", "inspector")
    search_fields = ("batch_no", "work_order__order_no", "inspector")
    autocomplete_fields = ("work_order",)
    inlines = [DefectRecordInline]
    date_hierarchy = "inspected_at"
    readonly_fields = ("created_at", "updated_at")

    @admin.display(description="不良率")
    def defect_rate_display(self, obj: Inspection) -> str:
        rate = obj.defect_rate
        # 不良率超过 5% 标红
        color = "#d32f2f" if rate > 0.05 else "#2e7d32"
        return format_html('<span style="color:{}">{:.2%}</span>', color, rate)


@admin.register(DefectRecord)
class DefectRecordAdmin(admin.ModelAdmin):
    list_display = ("inspection", "defect_type", "quantity", "cause")
    list_filter = ("defect_type",)
    search_fields = ("inspection__batch_no", "defect_type", "cause")
    autocomplete_fields = ("inspection",)

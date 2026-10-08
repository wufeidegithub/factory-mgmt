"""生产模块后台配置。"""

from django.contrib import admin
from django.utils.html import format_html

from apps.production.models import Product, ProductionReport, WorkOrder


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "spec", "unit")
    search_fields = ("code", "name", "spec")
    ordering = ("code",)


class ProductionReportInline(admin.TabularInline):
    model = ProductionReport
    extra = 0
    fields = ("reported_at", "quantity", "qualified_qty", "shift", "operator", "remark")


@admin.register(WorkOrder)
class WorkOrderAdmin(admin.ModelAdmin):
    list_display = (
        "order_no",
        "product",
        "plan_qty",
        "done_qty",
        "progress_bar",
        "status",
        "line",
        "due_date",
        "overdue_flag",
    )
    list_filter = ("status", "line", "due_date")
    search_fields = ("order_no", "product__code", "product__name")
    autocomplete_fields = ("product",)
    inlines = [ProductionReportInline]
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "updated_at", "progress")

    @admin.display(description="进度")
    def progress_bar(self, obj: WorkOrder) -> str:
        pct = round(obj.progress * 100)
        return format_html(
            '<div style="width:110px;background:#eee;border-radius:4px">'
            '<div style="width:{}%;background:#1976d2;height:14px;border-radius:4px"></div>'
            "</div><small>{}%</small>",
            pct,
            pct,
        )

    @admin.display(description="逾期", boolean=True)
    def overdue_flag(self, obj: WorkOrder) -> bool:
        return obj.is_overdue


@admin.register(ProductionReport)
class ProductionReportAdmin(admin.ModelAdmin):
    list_display = ("reported_at", "work_order", "quantity", "qualified_qty", "shift", "operator")
    list_filter = ("shift", "reported_at")
    search_fields = ("work_order__order_no", "operator")
    autocomplete_fields = ("work_order",)
    date_hierarchy = "reported_at"

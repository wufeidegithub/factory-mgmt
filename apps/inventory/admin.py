"""库存模块后台配置。"""

from django.contrib import admin
from django.utils.html import format_html

from apps.inventory.models import Material, StockMovement


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "category", "spec", "quantity", "safety_stock", "stock_state", "location")
    list_filter = ("category", "location")
    search_fields = ("code", "name", "spec", "supplier")
    ordering = ("code",)
    readonly_fields = ("created_at", "updated_at")

    @admin.display(description="库存状态")
    def stock_state(self, obj: Material) -> str:
        """低于安全库存标红，方便一眼扫出来。"""
        if obj.is_below_safety:
            return format_html('<b style="color:#d32f2f">低于安全库存</b>')
        return format_html('<span style="color:#2e7d32">正常</span>')


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ("occurred_at", "material", "movement_type", "quantity", "shift", "operator")
    list_filter = ("movement_type", "shift", "occurred_at")
    search_fields = ("material__code", "material__name", "operator", "remark")
    autocomplete_fields = ("material",)
    date_hierarchy = "occurred_at"
    readonly_fields = ("created_at", "updated_at")

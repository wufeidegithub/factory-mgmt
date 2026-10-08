"""设备模块后台配置。"""

from django.contrib import admin
from django.utils.html import format_html

from apps.equipment.models import Equipment, MaintenanceLog


class MaintenanceLogInline(admin.TabularInline):
    model = MaintenanceLog
    extra = 0
    fields = ("occurred_at", "log_type", "operator", "is_abnormal", "content", "next_date")


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "model", "location", "status_badge", "purchased_at", "next_maintenance", "due_flag")
    list_filter = ("status", "location")
    search_fields = ("code", "name", "model", "location")
    inlines = [MaintenanceLogInline]
    ordering = ("code",)

    @admin.display(description="保养到期", boolean=True)
    def due_flag(self, obj: Equipment) -> bool:
        return obj.is_due

    @admin.display(description="状态")
    def status_badge(self, obj: Equipment) -> str:
        palette = {
            "normal": "#2e7d32",
            "maintenance": "#ed6c02",
            "fault": "#d32f2f",
            "scrapped": "#757575",
        }
        color = palette.get(obj.status, "#333")
        return format_html('<b style="color:{}">{}</b>', color, obj.get_status_display())


@admin.register(MaintenanceLog)
class MaintenanceLogAdmin(admin.ModelAdmin):
    list_display = ("occurred_at", "equipment", "log_type", "operator", "is_abnormal", "cost", "next_date")
    list_filter = ("log_type", "is_abnormal", "occurred_at")
    search_fields = ("equipment__code", "equipment__name", "operator", "content")
    autocomplete_fields = ("equipment",)
    date_hierarchy = "occurred_at"

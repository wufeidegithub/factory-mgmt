"""人员模块后台配置。"""

from django.contrib import admin

from apps.hr.models import Employee, ShiftSchedule


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("emp_no", "name", "department", "position", "phone", "is_active")
    list_filter = ("department", "is_active")
    search_fields = ("emp_no", "name", "phone", "department")
    ordering = ("emp_no",)


@admin.register(ShiftSchedule)
class ShiftScheduleAdmin(admin.ModelAdmin):
    list_display = ("date", "employee", "shift", "line", "remark")
    list_filter = ("shift", "date", "line")
    search_fields = ("employee__emp_no", "employee__name", "line")
    autocomplete_fields = ("employee",)
    date_hierarchy = "date"
    # 排班量大，默认按日期倒序
    ordering = ("-date",)

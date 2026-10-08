"""人员与排班。"""

from django.db import models

from apps.core.models import Shift, TimeStampedModel


class Employee(TimeStampedModel):
    """员工档案。"""

    emp_no = models.CharField("工号", max_length=32, unique=True)
    name = models.CharField("姓名", max_length=64)
    department = models.CharField("部门", max_length=64, blank=True)
    position = models.CharField("岗位", max_length=64, blank=True)
    phone = models.CharField("联系电话", max_length=32, blank=True)
    hired_at = models.DateField("入职日期", null=True, blank=True)
    is_active = models.BooleanField("在职", default=True)

    class Meta(TimeStampedModel.Meta):
        verbose_name = "员工"
        verbose_name_plural = "员工"
        indexes = [models.Index(fields=["emp_no"])]

    def __str__(self) -> str:
        return f"{self.emp_no} {self.name}"


class ShiftSchedule(TimeStampedModel):
    """排班表。一人一天一条记录。"""

    employee = models.ForeignKey(
        Employee, verbose_name="员工", on_delete=models.CASCADE, related_name="schedules"
    )
    date = models.DateField("日期")
    shift = models.CharField("班次", max_length=16, choices=Shift.choices)
    line = models.CharField("生产线 / 工位", max_length=64, blank=True)
    remark = models.CharField("备注", max_length=200, blank=True)

    class Meta(TimeStampedModel.Meta):
        verbose_name = "排班"
        verbose_name_plural = "排班"
        # 同一人同一天只能排一个班次
        constraints = [
            models.UniqueConstraint(fields=["employee", "date"], name="uniq_employee_date"),
        ]
        indexes = [models.Index(fields=["date"])]

    def __str__(self) -> str:
        return f"{self.date} {self.employee.name} {self.get_shift_display()}"

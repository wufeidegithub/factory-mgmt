"""设备台账与点检维保。"""

from django.db import models

from apps.core.models import TimeStampedModel


class Equipment(TimeStampedModel):
    """设备台账。"""

    class Status(models.TextChoices):
        NORMAL = "normal", "正常"
        MAINTENANCE = "maintenance", "保养中"
        FAULT = "fault", "故障"
        SCRAPPED = "scrapped", "已报废"

    code = models.CharField("设备编号", max_length=32, unique=True)
    name = models.CharField("设备名称", max_length=100)
    model = models.CharField("规格型号", max_length=100, blank=True)
    location = models.CharField("安装位置", max_length=100, blank=True)
    status = models.CharField("状态", max_length=16, choices=Status.choices, default=Status.NORMAL)
    purchased_at = models.DateField("购入日期", null=True, blank=True)
    # 下次保养日期，看板据此提前提醒
    next_maintenance = models.DateField("下次保养日期", null=True, blank=True)

    class Meta(TimeStampedModel.Meta):
        verbose_name = "设备"
        verbose_name_plural = "设备"
        indexes = [models.Index(fields=["code"]), models.Index(fields=["status"])]

    def __str__(self) -> str:
        return f"{self.code} {self.name}"

    @property
    def is_due(self) -> bool:
        """是否到了保养期。"""
        from django.utils import timezone

        if not self.next_maintenance:
            return False
        return self.next_maintenance <= timezone.localdate()


class MaintenanceLog(TimeStampedModel):
    """点检 / 保养 / 维修记录。"""

    class LogType(models.TextChoices):
        DAILY_CHECK = "check", "日常点检"
        MAINTAIN = "maintain", "定期保养"
        REPAIR = "repair", "故障维修"

    equipment = models.ForeignKey(
        Equipment, verbose_name="设备", on_delete=models.CASCADE, related_name="logs"
    )
    log_type = models.CharField("类型", max_length=16, choices=LogType.choices)
    operator = models.CharField("执行人", max_length=64, blank=True)
    content = models.TextField("作业内容", blank=True)
    # 点检发现的异常项
    is_abnormal = models.BooleanField("是否异常", default=False)
    cost = models.DecimalField("费用", max_digits=12, decimal_places=2, default=0)
    occurred_at = models.DateTimeField("作业时间")
    next_date = models.DateField("下次计划日期", null=True, blank=True)

    class Meta(TimeStampedModel.Meta):
        verbose_name = "设备记录"
        verbose_name_plural = "设备记录"

    def __str__(self) -> str:
        return f"{self.equipment.code} {self.get_log_type_display()}"

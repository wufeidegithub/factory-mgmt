"""质量检验。"""

from django.db import models

from apps.core.models import TimeStampedModel


class Inspection(TimeStampedModel):
    """检验单。通常按批次开单，关联到工单。"""

    class Result(models.TextChoices):
        PENDING = "pending", "待检"
        PASS = "pass", "合格"
        FAIL = "fail", "不合格"
        CONCESSION = "concession", "让步接收"

    batch_no = models.CharField("批次号", max_length=32, unique=True)
    work_order = models.ForeignKey(
        "production.WorkOrder",
        verbose_name="关联工单",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="inspections",
    )
    sample_qty = models.DecimalField("抽检数量", max_digits=14, decimal_places=2, default=0)
    defect_qty = models.DecimalField("不良数量", max_digits=14, decimal_places=2, default=0)
    result = models.CharField("检验结论", max_length=16, choices=Result.choices, default=Result.PENDING)
    inspector = models.CharField("检验员", max_length=64, blank=True)
    inspected_at = models.DateTimeField("检验时间", null=True, blank=True)
    remark = models.TextField("备注", blank=True)

    class Meta(TimeStampedModel.Meta):
        verbose_name = "检验单"
        verbose_name_plural = "检验单"
        indexes = [models.Index(fields=["batch_no"]), models.Index(fields=["result"])]

    def __str__(self) -> str:
        return f"{self.batch_no} {self.get_result_display()}"

    @property
    def defect_rate(self) -> float:
        """不良率。"""
        if not self.sample_qty:
            return 0.0
        return float(self.defect_qty / self.sample_qty)


class DefectRecord(TimeStampedModel):
    """缺陷明细。一张检验单可以记录多个缺陷类型。"""

    inspection = models.ForeignKey(
        Inspection, verbose_name="检验单", on_delete=models.CASCADE, related_name="defects"
    )
    defect_type = models.CharField("缺陷类型", max_length=64)
    quantity = models.DecimalField("数量", max_digits=14, decimal_places=2, default=0)
    cause = models.CharField("原因分析", max_length=200, blank=True)
    action = models.CharField("处理措施", max_length=200, blank=True)

    class Meta(TimeStampedModel.Meta):
        verbose_name = "缺陷记录"
        verbose_name_plural = "缺陷记录"

    def __str__(self) -> str:
        return f"{self.defect_type} x{self.quantity}"

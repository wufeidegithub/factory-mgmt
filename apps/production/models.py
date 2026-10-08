"""生产工单与报工。"""

from django.db import models

from apps.core.models import Shift, TimeStampedModel


class Product(TimeStampedModel):
    """产品主数据。"""

    code = models.CharField("产品编码", max_length=32, unique=True)
    name = models.CharField("产品名称", max_length=100)
    spec = models.CharField("规格型号", max_length=100, blank=True)
    unit = models.CharField("单位", max_length=16, default="件")

    class Meta(TimeStampedModel.Meta):
        verbose_name = "产品"
        verbose_name_plural = "产品"

    def __str__(self) -> str:
        return f"{self.code} {self.name}"


class WorkOrder(TimeStampedModel):
    """生产工单。"""

    class Status(models.TextChoices):
        DRAFT = "draft", "草稿"
        RELEASED = "released", "已下达"
        IN_PROGRESS = "in_progress", "生产中"
        PAUSED = "paused", "暂停"
        DONE = "done", "已完工"
        CANCELLED = "cancelled", "已取消"

    order_no = models.CharField("工单号", max_length=32, unique=True)
    product = models.ForeignKey(
        Product, verbose_name="产品", on_delete=models.PROTECT, related_name="work_orders"
    )
    plan_qty = models.DecimalField("计划数量", max_digits=14, decimal_places=2)
    done_qty = models.DecimalField("已完成数量", max_digits=14, decimal_places=2, default=0)
    status = models.CharField("状态", max_length=16, choices=Status.choices, default=Status.DRAFT)
    line = models.CharField("生产线", max_length=32, blank=True)
    start_date = models.DateField("计划开工", null=True, blank=True)
    due_date = models.DateField("计划完工", null=True, blank=True)
    remark = models.TextField("备注", blank=True)

    class Meta(TimeStampedModel.Meta):
        verbose_name = "生产工单"
        verbose_name_plural = "生产工单"
        indexes = [models.Index(fields=["order_no"]), models.Index(fields=["status"])]

    def __str__(self) -> str:
        return f"{self.order_no} {self.product.name}"

    @property
    def progress(self) -> float:
        """完成进度 0~1。"""
        if not self.plan_qty:
            return 0.0
        return float(min(self.done_qty / self.plan_qty, 1))

    @property
    def is_overdue(self) -> bool:
        from django.utils import timezone

        if not self.due_date or self.status in {self.Status.DONE, self.Status.CANCELLED}:
            return False
        return self.due_date < timezone.localdate()


class ProductionReport(TimeStampedModel):
    """报工记录。一张工单可以有多条报工。"""

    work_order = models.ForeignKey(
        WorkOrder, verbose_name="工单", on_delete=models.CASCADE, related_name="reports"
    )
    quantity = models.DecimalField("报工数量", max_digits=14, decimal_places=2)
    qualified_qty = models.DecimalField("合格数量", max_digits=14, decimal_places=2, default=0)
    shift = models.CharField("班次", max_length=16, choices=Shift.choices, blank=True)
    operator = models.CharField("操作工", max_length=64, blank=True)
    reported_at = models.DateTimeField("报工时间")
    remark = models.CharField("备注", max_length=200, blank=True)

    class Meta(TimeStampedModel.Meta):
        verbose_name = "报工记录"
        verbose_name_plural = "报工记录"

    def __str__(self) -> str:
        return f"{self.work_order.order_no} 报工 {self.quantity}"

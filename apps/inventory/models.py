"""库存与物料管理。"""

from django.db import models

from apps.core.models import Shift, TimeStampedModel


class Material(TimeStampedModel):
    """物料主数据 + 当前库存。"""

    class Category(models.TextChoices):
        RAW = "raw", "原材料"
        PART = "part", "零部件"
        PACKAGE = "package", "包材"
        CONSUMABLE = "consumable", "耗材"

    code = models.CharField("物料编码", max_length=32, unique=True)
    name = models.CharField("物料名称", max_length=100)
    spec = models.CharField("规格型号", max_length=100, blank=True)
    category = models.CharField("类别", max_length=16, choices=Category.choices, default=Category.RAW)
    unit = models.CharField("单位", max_length=16, default="个")
    quantity = models.DecimalField("当前库存", max_digits=14, decimal_places=2, default=0)
    safety_stock = models.DecimalField("安全库存", max_digits=14, decimal_places=2, default=0)
    location = models.CharField("库位", max_length=64, blank=True)
    supplier = models.CharField("供应商", max_length=100, blank=True)

    class Meta(TimeStampedModel.Meta):
        verbose_name = "物料"
        verbose_name_plural = "物料"
        indexes = [models.Index(fields=["code"]), models.Index(fields=["category"])]

    def __str__(self) -> str:
        return f"{self.code} {self.name}"

    @property
    def is_below_safety(self) -> bool:
        """是否低于安全库存。"""
        return self.quantity < self.safety_stock


class StockMovement(TimeStampedModel):
    """出入库流水。库存变动一律通过这里记录，便于追溯。"""

    class MovementType(models.TextChoices):
        IN = "in", "入库"
        OUT = "out", "出库"
        ADJUST = "adjust", "盘点调整"

    material = models.ForeignKey(
        Material, verbose_name="物料", on_delete=models.PROTECT, related_name="movements"
    )
    movement_type = models.CharField("类型", max_length=10, choices=MovementType.choices)
    quantity = models.DecimalField("数量", max_digits=14, decimal_places=2)
    shift = models.CharField("班次", max_length=16, choices=Shift.choices, blank=True)
    operator = models.CharField("经办人", max_length=64, blank=True)
    remark = models.CharField("备注", max_length=200, blank=True)
    occurred_at = models.DateTimeField("发生时间")

    class Meta(TimeStampedModel.Meta):
        verbose_name = "出入库记录"
        verbose_name_plural = "出入库记录"

    def __str__(self) -> str:
        return f"{self.get_movement_type_display()} {self.material} {self.quantity}"

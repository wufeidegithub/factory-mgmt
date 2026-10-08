"""核心模块：公共抽象基类与枚举。

其他业务模块的模型都继承 TimeStampedModel，统一带上创建/更新时间和操作人。
页面视图放在 views.py，本文件只放数据模型。
"""

from django.conf import settings
from django.db import models


class TimeStampedModel(models.Model):
    """抽象基类：所有业务表共用。

    - created_at / updated_at 自动维护
    - created_by 记录操作人，便于追溯
    """

    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="创建人",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_created",
    )

    class Meta:
        abstract = True
        ordering = ["-created_at"]


class Shift(models.TextChoices):
    """班次。工厂场景几乎所有记录都要挂班次。"""

    MORNING = "morning", "早班"
    AFTERNOON = "afternoon", "中班"
    NIGHT = "night", "夜班"

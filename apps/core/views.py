"""核心模块视图：总看板。"""

from django.db.models import F
from django.shortcuts import render
from django.utils import timezone


def dashboard(request):
    """总看板：汇总各模块的关键指标。

    跨模块聚合放在这里而不是各模块内，避免 app 之间互相依赖。
    """
    from apps.equipment.models import Equipment
    from apps.inventory.models import Material
    from apps.production.models import WorkOrder
    from apps.quality.models import Inspection

    stats = [
        {
            "label": "进行中工单",
            "value": WorkOrder.objects.filter(status="in_progress").count(),
            "unit": "张",
        },
        {
            "label": "待检批次",
            "value": Inspection.objects.filter(result="pending").count(),
            "unit": "批",
        },
        {
            "label": "低于安全库存",
            "value": Material.objects.filter(quantity__lt=F("safety_stock")).count(),
            "unit": "种",
        },
        {
            "label": "异常设备",
            "value": Equipment.objects.exclude(status="normal").count(),
            "unit": "台",
        },
    ]

    context = {
        "today": timezone.localdate(),
        "stats": stats,
        "recent_orders": WorkOrder.objects.select_related("product").order_by("-created_at")[:10],
    }
    return render(request, "core/dashboard.html", context)

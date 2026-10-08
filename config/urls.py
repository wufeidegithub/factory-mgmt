"""URL 路由总表。

设计取舍：内部管理系统的大量增删改查直接复用 Django Admin，
只有需要自定义交互的页面（看板、报表）才写独立视图。
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # 自定义页面：看板与报表
    path("", include("apps.core.urls")),
]

# 后台站点标题（中文）
admin.site.site_header = "工厂管理系统"
admin.site.site_title = "工厂管理系统"
admin.site.index_title = "数据管理"

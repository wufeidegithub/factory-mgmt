"""核心模块路由。"""

from django.urls import path

from apps.core import views

app_name = "core"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
]

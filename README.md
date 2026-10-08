# 工厂管理系统

基于 Django 的工厂内部管理系统，覆盖 **物料库存、生产工单、质量检验、设备管理、人员排班** 五大模块。

## 技术栈

| 用途 | 选型 |
|---|---|
| Web 框架 | Django 5.x |
| 数据库 | 开发 SQLite / 生产 PostgreSQL |
| 后台管理 | Django Admin（深度定制） |
| 样式 | 原生 CSS + 自定义模板 |
| 静态文件 | WhiteNoise |
| 导出 | openpyxl |

## 目录结构

```
factory-mgmt/
├── manage.py               Django 命令行入口
├── config/                 项目配置
│   ├── settings.py         全部配置（读环境变量，区分开发/生产）
│   ├── urls.py             路由总表
│   ├── wsgi.py             生产部署入口
│   └── asgi.py             异步入口
├── apps/                   业务模块
│   ├── core/               公共抽象基类 + 总看板
│   ├── inventory/          物料库存、出入库流水
│   ├── production/         产品、工单、报工
│   ├── quality/            检验单、缺陷记录
│   ├── equipment/          设备台账、点检维保
│   └── hr/                 员工、排班
├── templates/              页面模板
│   ├── base.html           基础布局
│   └── core/dashboard.html 总看板
├── static/                 静态资源
│   └── css/style.css       自建页面样式
├── media/                  用户上传文件
├── logs/                   运行日志
├── scripts/                运维脚本
├── tests/                  测试
└── docs/                   文档
```

## 核心设计：Admin 优先

内部管理系统最大的成本是「为每个表写一套增删改查页面」，而这类页面彼此高度雷同。
本项目的取舍是：

- **增删改查全部交给 Django Admin** —— 只需在 `admin.py` 里配 `list_display` / `list_filter` / `search_fields`，立刻得到可用界面，还自带权限、导出、批量操作。
- **只有看板和报表才写自定义视图** —— 这类页面的交互 Admin 表达不了，放在 `apps/core/views.py`。

这样一来，新增一个业务模块的成本被压到很低。

## 数据模型概览

所有业务表继承 `apps/core/models.py` 的 `TimeStampedModel`，统一带 `created_at` / `updated_at` / `created_by`。

```
Product ──┐
          ├── WorkOrder ──┬── ProductionReport
          │               └── Inspection ── DefectRecord
Material ─┴── StockMovement

Equipment ──── MaintenanceLog
Employee  ──── ShiftSchedule
```

## 快速开始

```bash
# 1. 虚拟环境
python -m venv .venv
source .venv/Scripts/activate

# 2. 依赖
pip install -r requirements.txt

# 3. 环境变量（可选，开发默认值开箱即用）
cp .env.example .env

# 4. 建表
python manage.py makemigrations
python manage.py migrate

# 5. 建管理员账号
python manage.py createsuperuser

# 6. 启动
python manage.py runserver
```

打开 http://127.0.0.1:8000/ 看总看板，http://127.0.0.1:8000/admin/ 做数据维护。

## 部署到生产

```bash
# 关键环境变量
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=<随机长字符串>
DJANGO_ALLOWED_HOSTS=你的域名或内网IP
DB_ENGINE=postgres
DB_NAME=factory_mgmt
DB_USER=...
DB_PASSWORD=...

python manage.py collectstatic --noinput
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

前面再挂一层 Nginx 处理静态文件和 HTTPS。内网部署可以直接 gunicorn + WhiteNoise。

## 后续计划

- [ ] 工单数据导出 Excel
- [ ] 库存预警邮件/企业微信推送
- [ ] 设备保养到期自动提醒
- [ ] 生产日报图表（产量趋势、不良率趋势）
- [ ] 操作日志审计
- [ ] 权限分组（班组长 / 质检员 / 仓管 各自的可见范围）

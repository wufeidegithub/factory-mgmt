#!/usr/bin/env python
"""Django 命令行入口。

    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver
"""

import os
import sys
from pathlib import Path


def main() -> None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

    # 项目根加入 sys.path，保证 config / apps 可导入
    root = Path(__file__).resolve().parent
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

    try:
        from django.core.management import execute_from_command_line
    except ImportError as e:
        raise ImportError(
            "无法导入 Django，请先执行：pip install -r requirements.txt"
        ) from e

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()

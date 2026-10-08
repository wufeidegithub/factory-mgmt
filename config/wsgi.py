"""WSGI 入口（生产部署用，如 gunicorn / uwsgi）。"""

import os
from pathlib import Path
import sys

# gunicorn 启动时工作目录可能不在项目根，这里显式补上
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

from django.core.wsgi import get_wsgi_application  # noqa: E402

application = get_wsgi_application()

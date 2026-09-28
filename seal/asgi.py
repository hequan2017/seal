import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "seal.settings")
django.setup()

# channels 4：ASGI 入口直接复用 seal/routing.py 中定义的 application
from seal.routing import application  # noqa: E402

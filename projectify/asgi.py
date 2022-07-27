"""
ASGI config for projectify project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import (
    get_asgi_application,
)

from channels.auth import (
    AuthMiddlewareStack,
)
from channels.routing import (
    ProtocolTypeRouter,
    URLRouter,
)

from django.urls import path, re_path

import django_eventstream


os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "projectify.settings.production"
)
asgi_application = get_asgi_application()

from .urls import (  # noqa: E402
    websocket_urlpatterns,
)


websocket_application = AuthMiddlewareStack(URLRouter(websocket_urlpatterns))

application = ProtocolTypeRouter(
    {
        "http": URLRouter(
            [
                path(
                    "events/",
                    AuthMiddlewareStack(
                        URLRouter(django_eventstream.routing.urlpatterns)
                    ),
                    {"channels": ["test"]},
                ),
                re_path(r"", get_asgi_application()),
            ]
        ),
        "websocket": websocket_application,
    }
)

"""
projectify URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import (
    settings,
)
from django.conf.urls.static import (
    static,
)
from django.contrib import (
    admin,
)
from django.urls import (
    include,
    path,
)
from django.views.decorators import (
    csrf,
)

import django_eventstream

from workspace.consumers import (
    TaskConsumer,
    WorkspaceBoardConsumer,
    WorkspaceConsumer,
)

from . import (
    schema,
)
from .views import (
    GraphQLBatchView,
    GraphQLView,
)


urlpatterns = (
    path("admin/", admin.site.urls),
    path(
        "graphql",
        csrf.csrf_exempt(
            GraphQLView.as_view(
                schema=schema.schema,
                graphiql=settings.GRAPHIQL_ENABLE,
            ),
        ),
        name="graphql",
    ),
    path(
        "graphql-batch",
        csrf.csrf_exempt(
            GraphQLBatchView.as_view(
                schema=schema.schema,
                graphiql=settings.GRAPHIQL_ENABLE,
            ),
        ),
        name="graphql-batch",
    ),
    path(
        r"premail/",
        include("premail.urls"),
    ),
    path(
        r"user/",
        include("user.urls"),
    ),
    path(
        "workspace/",
        include("workspace.urls"),
    ),
    path("blog/api/v1/", include("blog.urls")),
    path("corporate/", include("corporate.urls")),
)

if settings.SERVE_MEDIA:
    urlpatterns = (
        *urlpatterns,
        *static(
            settings.MEDIA_URL,
            document_root=settings.MEDIA_ROOT,
        ),
    )

if settings.DEBUG_TOOLBAR:
    urlpatterns = (
        *urlpatterns,
        path("__debug__/", include("debug_toolbar.urls")),
    )

websocket_urlpatterns = (
    path("ws/task/<uuid:uuid>/", TaskConsumer.as_asgi()),
    path("ws/workspace-board/<uuid:uuid>/", WorkspaceBoardConsumer.as_asgi()),
    path("ws/workspace/<uuid:uuid>/", WorkspaceConsumer.as_asgi()),
)

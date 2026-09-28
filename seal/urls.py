from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from system.views import index
from rest_framework.authtoken import views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from graphene_django.views import GraphQLView
from seal.schema import schema

urlpatterns = [
    path('', index),
    path('index', index, name="index"),
    path('system/', include('system.urls', namespace='system')),
    path('assets/', include('assets.urls', namespace='assets')),
    path('k8s/', include('k8s.urls', namespace='k8s')),
    path('admin/', admin.site.urls, ),
    path('api/token', views.obtain_auth_token),
    # Swagger UI 与 OpenAPI Schema（drf-spectacular，替代已停维的 django-rest-swagger）
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='docs2'), name="docs"),
    path('api/docs2/', SpectacularAPIView.as_view(), name="docs2"),
    path('graphql/', GraphQLView.as_view(graphiql=True, schema=schema)),

    path('sql/', include('sql.urls', namespace='sql')),
]

from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from system.views import index
from rest_framework.authtoken import views
from rest_framework.documentation import include_docs_urls
from graphene_django.views import GraphQLView
from seal.schema import schema
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='海豹 API 文档')

API_TITLE = '海豹 API 文档'
API_DESCRIPTION = '海豹 API 文档'

urlpatterns = [
    path('', index),
    path('index', index, name="index"),
    path('system/', include('system.urls', namespace='system')),
    path('assets/', include('assets.urls', namespace='assets')),
    path('k8s/', include('k8s.urls', namespace='k8s')),
    path('admin/', admin.site.urls, ),
    path('api/token', views.obtain_auth_token),
    path('api/docs/', include_docs_urls(title=API_TITLE, description=API_DESCRIPTION, authentication_classes=[],
                                        permission_classes=[])),
    path('api/docs2/', schema_view, name="docs"),
    path('graphql/', GraphQLView.as_view(graphiql=True, schema=schema)),

    path('sql/', include('sql.urls', namespace='sql')),
]

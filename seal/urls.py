from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from system.views import index
from rest_framework.authtoken import views
from rest_framework.documentation import include_docs_urls

API_TITLE = '海豹 API 文档'
API_DESCRIPTION = '海豹 API 文档'

urlpatterns = [
    path('', index),
    path('index', index, name="index"),
    path('system/', include('system.urls', namespace='system')),
    path('assets/', include('assets.urls', namespace='assets')),
    path('admin/', admin.site.urls, ),
    path('api/token', views.obtain_auth_token),
    path('api/docs/', include_docs_urls(title=API_TITLE, description=API_DESCRIPTION, authentication_classes=[],
                                        permission_classes=[]))
]

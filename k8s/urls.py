from django.urls import path
from k8s import views
app_name = "k8s"

urlpatterns = [
    path('k8s-pod-list', views.K8sPodListView.as_view(), name='k8s-pod-list'),
    path('k8s-pod-webssh', views.K8sPodWebssh.as_view(), name='k8s-pod-webssh')
]

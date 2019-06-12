from django.urls import path
from k8s import views

app_name = "k8s"

urlpatterns = [
    path('k8s-node-list', views.K8sNodeListView.as_view(), name='k8s-node-list'),

    path('k8s-service-list', views.K8sServiceListView.as_view(), name='k8s-service-list'),

    path('k8s-pod-list', views.K8sPodListView.as_view(), name='k8s-pod-list'),
    path('k8s-pod-webssh', views.K8sPodWebssh.as_view(), name='k8s-pod-webssh'),
    path('k8s-pod-detail', views.K8sPodDetail.as_view(), name='k8s-pod-detail')
]

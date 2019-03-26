from django.urls import path
from assets import views

app_name = "assets"

urlpatterns = [
    path('ecs-create', views.EcsCreateView.as_view(), name='ecs-create'),
    path('ecs-list', views.EcsListView.as_view(), name='ecs-list'),
    path('ecs-update-<int:pk>', views.EcsUpdateView.as_view(), name='ecs-update'),
    path('ecs-detail-<int:pk>', views.EcsDetailView.as_view(), name='ecs-detail'),
    path('ecs-delete', views.EcsDeleteView.as_view(), name='ecs-delete'),


    path('api/ecs', views.ApiEcsList.as_view()),
    path('api/ecs/<int:pk>', views.ApiEcsDetail.as_view()),
]

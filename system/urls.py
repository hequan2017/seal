from django.urls import path
from system.views import login_view, UserPasswordUpdateView, logout_view, UserInfo

app_name = "system"

urlpatterns = [
    path('login', login_view, name="login"),
    path('password_update', UserPasswordUpdateView.as_view(), name="password_update"),
    path('logout', logout_view, name="logout"),


    path('api/user_info', UserInfo.as_view()),
    path('api/logout', UserInfo.as_view())
]

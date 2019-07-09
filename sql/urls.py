from django.urls import path
from sql import views

app_name = "sql"

urlpatterns = [
    path('sql.html', views.SqlDdl.as_view(), name='sql_ddl'),
    path('sql-<str:pk>.html', views.SqlDdlQuery.as_view(), name='sql_query'),
]

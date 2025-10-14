# analytics/urls.py
from django.urls import path
from . import admin

urlpatterns = [
    path('', admin.index, name="admin_analytics_index"),
    path('revenue-data/', admin.revenue_data, name="admin_revenue_data"),
]

from django.urls import path
from . import admin

urlpatterns = [
    path('',admin.index,name='admin_revenue_report_index')
]


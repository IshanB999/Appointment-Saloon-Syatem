from django.urls import path
from . import admin

urlpatterns = [
    path('', admin.index, name='admin_service_index'),
    path('store/', admin.store, name='admin_service_store'),
    path('delete/', admin.delete, name='admin_service_delete'),
]

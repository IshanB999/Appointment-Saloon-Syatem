from django.urls import path, include
from . import admin

urlpatterns = [
    path('', admin.index , name='admin_outlet_index' ),
    path('create/', admin.create, name='admin_outlet_create'),
    path('store/', admin.store, name='admin_outlet_store'),
    path('edit/', admin.edit, name='admin_outlet_edit'),
    path('update/', admin.update, name='admin_outlet_update'),
    path('delete/', admin.delete, name='admin_outlet_delete'),
     path('<int:outlet_id>/services/', admin.outlet_service_list, name="admin_outlet_service_list"),
]   
from django.urls import path
from . import admin  # views in outlets/admin.py

urlpatterns = [
    path('', admin.index, name='admin_outlet_index'),  # /admin/outlets/
    path('create/', admin.create, name='admin_outlet_create'),  # /admin/outlets/create/
    path('edit/', admin.edit, name='admin_outlet_edit'),        # /admin/outlets/edit/
    path('delete/', admin.delete, name='admin_outlet_delete'),  # /admin/outlets/delete/
    path('<int:outlet_id>/services/', admin.outlet_service_list, name='admin_outlet_service_list'),
    path('<int:outlet_id>/slot-management/', admin.outlet_slot_management, name='admin_outlet_slot_management'),
    path('complete-booking/<int:booking_id>/', admin.complete_booking, name='admin_complete_booking'),
    path('update-booking-status/<int:booking_id>/', admin.change_booking_status, name='admin_change_booking_status'),
]

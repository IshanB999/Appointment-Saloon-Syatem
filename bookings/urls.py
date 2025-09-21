from django.urls import path, include
from . import admin

urlpatterns = [
    path('', admin.index , name='admin_booking_index'),
    path('booking-detail/', admin.detail , name='admin_booking_detail'),
    # path('delete', admin.delete_booking, name='admin_booking_delete'),
]
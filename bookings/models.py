import os
from django.db import models
from django_softdelete.models import SoftDeleteModel
from outlets.models import Outlet
from service.models import Service


class Booking(SoftDeleteModel, models.Model):
    created_by = models.IntegerField(null=True)
    updated_by = models.IntegerField(null=True)
    deleted_by = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    mobile_no = models.CharField(max_length=255, null=True, blank=True)
    outlet = models.ForeignKey(Outlet, on_delete=models.CASCADE, null=True, blank=True)
    booking_date = models.DateField(null=True, blank=True) 
    booking_time = models.TimeField(null=True, blank=True)
    booking_message = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = "db_bookings"


class BookingService(SoftDeleteModel, models.Model):
    created_by = models.IntegerField(null=True)
    updated_by = models.IntegerField(null=True)
    deleted_by = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, blank=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = "db_booking_services"

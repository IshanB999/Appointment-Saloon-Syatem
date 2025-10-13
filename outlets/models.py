import os
from django.db import models
from django_softdelete.models import SoftDeleteModel
from service.models import Service
from datetime import time as dt_time


class Outlet(SoftDeleteModel, models.Model):
    created_by = models.IntegerField(null=True)
    updated_by = models.IntegerField(null=True)
    deleted_by = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    address = models.TextField(null=True, blank=True)   
    phone = models.CharField(max_length=255, null=True, blank=True)
    mobile = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='outlets/', null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.CharField(max_length=255, null=True, blank=True)
    longitude = models.CharField(max_length=255, null=True, blank=True)
    sort_order = models.IntegerField(null=True, blank=True)
    
    total_slots = models.PositiveIntegerField(
        default=6,
        help_text="Maximum concurrent bookings (default 6)"
    )
    opening_time = models.TimeField(
        default=dt_time(hour=10, minute=0),
        help_text="Default opening time"
    )
    closing_time = models.TimeField(
        default=dt_time(hour=18, minute=0),
        help_text="Default closing time"
    )
    is_closed = models.BooleanField(
        default=False,
        help_text="If true, outlet is closed for bookings"
    )
    class Meta:
        db_table = "db_outlets"

    def __str__(self):
        return self.name or f"Outlet{self.pk}"


class OutletServicePrice(models.Model):
    outlet = models.ForeignKey(Outlet, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "db_outlet_service_prices"
        unique_together = ("outlet", "service")

    def __str__(self):
        return f"{self.outlet.name} - {self.service.name} ({self.price})"
    

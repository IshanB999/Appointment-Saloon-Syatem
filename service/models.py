import os
from django.db import models
from django_softdelete.models import SoftDeleteModel

class Service(SoftDeleteModel, models.Model):
    created_by = models.IntegerField(null=True)
    updated_by = models.IntegerField(null=True)
    deleted_by = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    code = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=255, null=True, blank=True)

    class Meta: 
        db_table = "db_services"

    def __str__(self):
        return self.name or "Unnamed Service"

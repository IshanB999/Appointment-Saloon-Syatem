from django.urls import path
from . import admin  # your admin views

urlpatterns = [
    path('', admin.index, name='admin_employees_index'),  # List employees
    path('add/', admin.add_employee, name='admin_add_employee'),  # Add employee page
    path('delete/<int:id>/', admin.delete_employee, name='admin_employees_delete'),  # Delete employee
]

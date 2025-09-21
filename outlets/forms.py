from django import forms
from .models import Outlet

class OutletForm(forms.ModelForm):
    class Meta:
        model = Outlet
        fields = ['name', 'address', 'phone', 'mobile', 'email', 'image', 'status', 'sort_order']

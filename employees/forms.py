from django import forms
from .models import Employees

class EmployeeForm(forms.ModelForm):
    same_as_temp = forms.BooleanField(required=False, label="Permanent address same as temporary")

    class Meta:
        model = Employees
        fields = ['first_name','last_name','phone_number','email','gender',
                  'temp_address','perm_address','country','zip_code',
                  'joining_date','photo','role','outlet']
        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'phone_number': forms.TextInput(attrs={'class':'form-control'}),
            'temp_address': forms.Textarea(attrs={'class':'form-control', 'rows':2}),
            'perm_address': forms.Textarea(attrs={'class':'form-control', 'rows':2}),
            'country': forms.TextInput(attrs={'class':'form-control'}),
            'zip_code': forms.TextInput(attrs={'class':'form-control'}),
            'joining_date': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            'photo': forms.ClearableFileInput(attrs={'class':'form-control'}),
            'role': forms.Select(attrs={'class':'form-control'}),
            'outlet': forms.Select(attrs={'class':'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        temp_address = cleaned_data.get('temp_address')
        same_as_temp = cleaned_data.get('same_as_temp')
        if same_as_temp and temp_address:
            cleaned_data['perm_address'] = temp_address
        return cleaned_data

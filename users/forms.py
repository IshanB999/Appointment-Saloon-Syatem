from django import forms
from django.core.exceptions import ValidationError

from users.models import NewUser


class UserForm(forms.Form):
    email = forms.EmailField()
    username = forms.CharField(max_length=255)
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)

    def clean(self):
        email = self.cleaned_data.get('email')
        if NewUser.objects.filter(email=email).exists():
            raise ValidationError("Email exists")
        return self.cleaned_data


class UpdateUserForm(forms.Form):
    email = forms.EmailField()
    # username = forms.CharField(max_length=255)
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)

    # def clean(self):
    #     email = self.cleaned_data.get('email')
    #     if NewUser.objects.filter(email=email).exists():
    #         raise ValidationError("Email exists")
    #     return self.cleaned_data


class RoleForm(forms.Form):
    name = forms.CharField(max_length=255)


class ContentTypeForm(forms.Form):
    name = forms.CharField(max_length=255)
    module = forms.CharField(max_length=255)


class PermissionForm(forms.Form):
    permission = forms.CharField(max_length=255)
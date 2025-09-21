from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from outlets.models import Outlet



class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        if other_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must be assigned to is_staff=True'))

        if other_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must be assigned to is_superuser=True'))

        return self.create_user(email, password, **other_fields)

    def create_user(self, email, password, **other_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.save()
        return user


class NewUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=255, unique=True,default='anonymous')
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(default=timezone.now)
    token = models.CharField(max_length=6, null=True, blank=True)
    objects = CustomAccountManager()
    last_login_date = models.DateTimeField(null=True, blank=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    last_activity = models.DateTimeField(null=True, blank=True)
    uer_hash_code = models.CharField(max_length=255, null=True, blank=True)
    is_social = models.BooleanField(default=False)
    platform = models.CharField(max_length=255, null=True, blank=True)
    outlet = models.ForeignKey(Outlet, on_delete=models.CASCADE, null=True, blank=True)
    USERNAME_FIELD = 'email'

    class Meta:
        db_table = "aauth_users"
    # def __str__(self):
    #     return self.email
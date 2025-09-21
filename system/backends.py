from django.contrib.auth.backends import ModelBackend
from django.utils import timezone
from django.http import HttpResponse


class CustomAuthenticationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = super().authenticate(request, username, password, **kwargs)
        if user:
            user.last_login_ip = request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('HTTP_X_REAL_IP') or request.META.get('REMOTE_ADDR')
            user.last_login_date = timezone.now()
            user.last_activity = timezone.now()
            user.save()
        return user
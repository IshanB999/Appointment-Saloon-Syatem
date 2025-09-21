from django.urls import path, include
from administrator import views, admin

urlpatterns = [
    path('', admin.index, name='member_home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('users/', include('users.urls')),
    path('api/booking-events/', admin.booking_events, name='booking_events'),
    path('outlets/', include('outlets.urls')),
    path('services/', include('service.urls')),
    path('bookings/', include('bookings.urls')),
    path('employees/', include('employees.urls')),
]
from django.urls import path, include
from frontend import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name='public_home'),
    path('store-booking', views.book_appointment, name='store_appointment_booking'),
    path('get_services_for_outlet/', views.get_services_for_outlet, name='get_services_for_outlet'),
]
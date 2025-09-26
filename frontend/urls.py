from django.urls import path
from frontend import views

urlpatterns = [
    path('', views.index, name='public_home'),
    path('store-booking/', views.book_appointment, name='store_appointment_booking'),
    path('get_services_for_outlet/', views.get_services_for_outlet, name='get_services_for_outlet'),
    path('payment/<int:booking_id>/', views.payment_page, name='payment_page'),
    path('pay-cash/<int:booking_id>/', views.pay_cash, name='pay_cash'),
    path('pay-esewa/<int:booking_id>/', views.pay_esewa, name='pay_esewa'),
    # path('pay-esewa/<int:booking_id>/', views.pay_esewa, name='pay_esewa'),
    path("esewa-success/<int:booking_id>/", views.esewa_success, name="esewa_success"),

    path('esewa/failure/', views.esewa_failure, name='esewa_failure'),

]

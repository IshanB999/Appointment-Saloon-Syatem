from django.shortcuts import render
from django.http import JsonResponse
from bookings.models import Booking
from outlets.models import Outlet
from datetime import date, timedelta
from django.db import models
from calendar import monthrange

def index(request):
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())
    start_of_last_week = start_of_week - timedelta(days=7)
    end_of_last_week = start_of_week - timedelta(days=1)
    start_of_month = today.replace(day=1)
    last_month_last_day = start_of_month - timedelta(days=1)
    start_of_last_month = last_month_last_day.replace(day=1)

    total_bookings = Booking.objects.count()
    bookings_this_week = Booking.objects.filter(booking_date__gte=start_of_week, booking_date__lte=today).count()
    bookings_last_week = Booking.objects.filter(booking_date__gte=start_of_last_week, booking_date__lte=end_of_last_week).count()
    bookings_this_month = Booking.objects.filter(booking_date__gte=start_of_month, booking_date__lte=today).count()
    bookings_last_month = Booking.objects.filter(booking_date__gte=start_of_last_month, booking_date__lte=last_month_last_day).count()

    # Bookings per outlet
    bookings_per_outlet_this_week = Booking.objects.filter(booking_date__gte=start_of_week, booking_date__lte=today) \
        .values('outlet__name') \
        .annotate(count=models.Count('id')).order_by('-count')

    bookings_per_outlet_last_week = Booking.objects.filter(booking_date__gte=start_of_last_week, booking_date__lte=end_of_last_week) \
        .values('outlet__name') \
        .annotate(count=models.Count('id')).order_by('-count')

    context = {
        "total_bookings": total_bookings,
        "bookings_this_week": bookings_this_week,
        "bookings_last_week": bookings_last_week,
        "bookings_this_month": bookings_this_month,
        "bookings_last_month": bookings_last_month,
        "bookings_per_outlet_this_week": bookings_per_outlet_this_week,
        "bookings_per_outlet_last_week": bookings_per_outlet_last_week,
    }

    return render(request, "analytics/index.html", context)


def revenue_data(request):
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())
    start_of_last_week = start_of_week - timedelta(days=7)
    end_of_last_week = start_of_week - timedelta(days=1)
    start_of_month = today.replace(day=1)
    last_month_last_day = start_of_month - timedelta(days=1)
    start_of_last_month = last_month_last_day.replace(day=1)

    outlets = Outlet.objects.all()
    revenue_last_week = []
    revenue_last_month = []

    for outlet in outlets:
        bookings_week = Booking.objects.filter(outlet=outlet, booking_date__gte=start_of_week, booking_date__lte=today)
        revenue_week = sum([b.total_price for b in bookings_week])
        revenue_last_week.append({'outlet': outlet.name, 'revenue': revenue_week})

        bookings_month = Booking.objects.filter(outlet=outlet, booking_date__gte=start_of_last_month, booking_date__lte=last_month_last_day)
        revenue_month = sum([b.total_price for b in bookings_month])
        revenue_last_month.append({'outlet': outlet.name, 'revenue': revenue_month})

    # Revenue trend over 12 months
    current_year = today.year
    revenue_trend = []
    for month in range(1, 13):
        first_day = date(current_year, month, 1)
        last_day = date(current_year, month, monthrange(current_year, month)[1])
        month_total = sum([b.total_price for b in Booking.objects.filter(booking_date__gte=first_day, booking_date__lte=last_day)])
        revenue_trend.append({'month': first_day.strftime('%b'), 'revenue': month_total})

    return JsonResponse({
        'last_week': revenue_last_week,
        'last_month': revenue_last_month,
        'trend': revenue_trend
    })

from datetime import date, timedelta
from django.shortcuts import render
from bookings.models import Booking
from outlets.models import Outlet


def index(request):
    """
    Revenue report view with date range filter,
    revenue per outlet, booking summary per outlet,
    and completed bookings table.
    """
    # Get start and end dates from query params
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    # Convert to date or set default (last 30 days)
    if start_date_str and end_date_str:
        start_date = date.fromisoformat(start_date_str)
        end_date = date.fromisoformat(end_date_str)
    else:
        end_date = date.today()
        start_date = end_date - timedelta(days=30)

    # All bookings within range
    bookings = Booking.objects.filter(
        booking_date__gte=start_date,
        booking_date__lte=end_date
    )

    # Only completed bookings are considered for revenue
    completed_bookings = bookings.filter(status='Completed')
    total_revenue = sum(b.total_price for b in completed_bookings)

    # Revenue and summary per outlet
    outlets = Outlet.objects.all()
    revenue_per_outlet = []
    summary_per_outlet = []

    for outlet in outlets:
        outlet_bookings = bookings.filter(outlet=outlet)
        outlet_completed = outlet_bookings.filter(status='Completed').count()
        outlet_pending = outlet_bookings.filter(status='Pending').count()
        outlet_cancelled = outlet_bookings.filter(status='Cancelled').count()

        # Revenue only from completed bookings
        revenue = sum(b.total_price for b in outlet_bookings.filter(status='Completed'))

        revenue_per_outlet.append({
            'outlet': outlet.name,
            'revenue': revenue
        })

        summary_per_outlet.append({
            'outlet': outlet.name,
            'completed': outlet_completed,
            'pending': outlet_pending,
            'cancelled': outlet_cancelled
        })

    context = {
        'start_date': start_date,
        'end_date': end_date,
        'total_revenue': total_revenue,
        'revenue_per_outlet': revenue_per_outlet,
        'summary_per_outlet': summary_per_outlet,
        'bookings': completed_bookings,  # Only completed bookings are shown in the table
    }

    return render(request, 'revenue_report/index.html', context)

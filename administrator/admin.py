from django.contrib import admin
from django.shortcuts import render
# Register your models here.
from system.decorators import unauthenticated_user, allowed_users, check_member
from django.db.models import Sum, Count
import re
import json
from django.utils.safestring import mark_safe
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db.models import Count, Q
from io import BytesIO
from django.views.decorators.csrf import csrf_exempt
from bookings.models import Booking, BookingService 
from django.db.models import Prefetch
from service.models import Service
from django.utils import timezone
from django.utils.dateparse import parse_date, parse_datetime
from datetime import timedelta

 
@unauthenticated_user
@check_member
def index(request):
    today = timezone.localdate()
    month_start = today.replace(day=1)

    # Start with all bookings
    base_qs = Booking.objects.all()

    # Prefer outlet from check_member (if provided)
    outlet = getattr(request, "outlet", None)

    # If not set, but user is in Outlet Group, fall back to user's own outlet
    if not outlet and request.user.is_authenticated and request.user.groups.filter(name__iexact='Outlet Group').exists():
        outlet = getattr(request.user, "outlet", None)

    # Apply scoping if an outlet is available
    if outlet:
        base_qs = base_qs.filter(outlet=outlet)

    counts = {
        "today": base_qs.filter(booking_date=today).count(),
        "month": base_qs.filter(booking_date__gte=month_start, booking_date__lte=today).count(),
        "total": base_qs.count(),
    }
    return render(request, "main_view/templates/index.html", {"counts": counts})



@unauthenticated_user
@check_member
def booking_events(request):
    """
    Returns bookings as FullCalendar events.
    Accepts FullCalendar's ?start=...&end=... which are ISO datetimes.
    """
    def _parse_fc_bound(s: str):
        if not s:
            return None
        dt = parse_datetime(s)
        if dt:
            if timezone.is_naive(dt):
                try:
                    dt = timezone.make_aware(dt, timezone.get_current_timezone())
                except Exception:
                    pass
            return dt.date()
        d = parse_date(s) or parse_date(s[:10])
        return d

    start_param = request.GET.get("start")
    end_param   = request.GET.get("end")
    start_date  = _parse_fc_bound(start_param)
    end_date    = _parse_fc_bound(end_param)

    # ---------- SCOPED BASE QUERYSET ----------
    qs = (
        Booking.objects
        .select_related("outlet")
        .prefetch_related(
            Prefetch(
                "bookingservice_set",
                queryset=BookingService.objects.select_related("service").only("service__id", "service__name")
            )
        )
    )

    # Prefer outlet from check_member (request.outlet)
    outlet = getattr(request, "outlet", None)

    # If not set, but user is in Outlet Group, fall back to user's own outlet
    if not outlet and request.user.is_authenticated and request.user.groups.filter(name__iexact='Outlet Group').exists():
        outlet = getattr(request.user, "outlet", None)

    # Apply scoping if outlet is available
    if outlet:
        qs = qs.filter(outlet=outlet)

    # ---------- DATE WINDOW FILTER ----------
    # FullCalendar's `end` is exclusive
    if start_date and end_date:
        qs = qs.filter(booking_date__gte=start_date, booking_date__lt=end_date)
    elif start_date:
        qs = qs.filter(booking_date__gte=start_date)
    elif end_date:
        qs = qs.filter(booking_date__lt=end_date)

    status_colors = {
        "pending":   "#f6c343",
        "confirmed": "#28a745",
        "cancelled": "#6c757d",
    }

    events = []
    for b in qs:
        if not b.booking_date:
            continue

        service_names = [bs.service.name for bs in b.bookingservice_set.all() if getattr(bs.service, "name", None)]
        parts = [b.full_name or "Booking"]
        if service_names:
            parts.append(", ".join(service_names))
        if b.outlet and b.outlet.name:
            parts.append(f"@ {b.outlet.name}")
        title = " • ".join(parts)

        if b.booking_time:
            start_combined = timezone.datetime.combine(b.booking_date, b.booking_time)
            # ensure awareness
            if timezone.is_naive(start_combined):
                start_dt = timezone.make_aware(start_combined, timezone.get_current_timezone())
            else:
                start_dt = start_combined
            end_dt = start_dt + timedelta(hours=1)

            events.append({
                "id": b.id,
                "title": title,
                "start": start_dt.isoformat(),
                "end": end_dt.isoformat(),
                "allDay": False,
                "color": status_colors.get((b.status or "").lower()),
                "url": f"/admin/bookings/booking-detail?id={b.id}",
            })
        else:
            events.append({
                "id": b.id,
                "title": title,
                "start": b.booking_date.isoformat(),
                "allDay": True,
                "color": status_colors.get((b.status or "").lower()),
                "url": f"/admin/bookings/booking-detail?id={b.id}",
            })

    return JsonResponse(events, safe=False)

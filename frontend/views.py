from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from django.views.decorators.http import require_http_methods
from system.wordpress import get_wp_header_full, get_wp_footer_full
from outlets.models import Outlet
from service.models import Service
from bookings.models import Booking, BookingService
from django.http import HttpResponse
from system.send_whatsapp_twilio import send_booking_alert, build_whatsapp_url
from django.conf import settings
from django.utils.dateparse import parse_date, parse_time
from django.db import transaction
from django.db.models.functions import Lower
from django.http import JsonResponse
from outlets.models import OutletServicePrice
from service.models import Service

@require_http_methods(["GET", "POST"])
def index(request):
    outlets = Outlet.objects.all().order_by('name')
    services = (
        Service.objects
        .all() 
        .order_by(Lower('gender'), 'name') 
    )
    context = {
        "wp_header_full": mark_safe(get_wp_header_full()),
        "wp_footer_full": mark_safe(get_wp_footer_full()),
        "outlets": outlets,
        "services": services,
        "title": "Home Page",
    }
    return render(request, "frontend/templates/appointment/index.html", context)


@require_http_methods(["POST"])
def book_appointment(request):
    base_url = settings.WP_BASE.rstrip("/")
    data = request.POST
    full_name   = (data.get("full_name") or "").strip()
    email       = (data.get("email") or "").strip()
    mobile_no   = (data.get("mobile_no") or "").strip()
    outlet_id   = data.get("outlet")
    service_ids = data.getlist("services")  # multiple checkboxes share the same name
    d_str       = data.get("booking_date")
    t_str       = data.get("booking_time")
    booking_date = parse_date(d_str) if d_str else None
    booking_time = parse_time(t_str) if t_str else None
    outlet = Outlet.objects.filter(pk=outlet_id).first()
    wanted_ids = {int(sid) for sid in service_ids}
    services = list(Service.objects.filter(id__in=wanted_ids).only("id"))
    try:
        with transaction.atomic():
            booking = Booking.objects.create(
                full_name=full_name,
                email=email or None,
                mobile_no=mobile_no,
                outlet=outlet,
                booking_date=booking_date,
                booking_time=booking_time,
                status="pending",
            )

            BookingService.objects.bulk_create(
                [BookingService(booking=booking, service=s) for s in services],
                ignore_conflicts=False,
            )
        service_names = ", ".join(s.name for s in services if s.name)
        msg = (
            f"Hello! I'd like to confirm my appointment.\n"
            f"Name: {full_name}\n"
            f"Phone: {mobile_no}\n"
            f"Service: {service_names}"
        )
        url = build_whatsapp_url(f'+977{outlet.mobile}', msg)
        return redirect(url)

    except Exception as e:
        return redirect(base_url)
    



def get_services_for_outlet(request):
    outlet_id = request.GET.get("outlet_id")
    if not outlet_id:
        return JsonResponse({"ladies": [], "gents": []})

    services = OutletServicePrice.objects.filter(outlet_id=outlet_id).select_related('service')

    ladies = [
        {"id": sp.service.id, "name": sp.service.name}
        for sp in services
        if sp.service.gender.lower() == "ladies"
    ]
    gents  = [
        {"id": sp.service.id, "name": sp.service.name}
        for sp in services
        if sp.service.gender.lower() == "gents"
    ]

    return JsonResponse({"ladies": ladies, "gents": gents})


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
from django.shortcuts import get_object_or_404
import uuid
import hmac
import base64
import hashlib
from decimal import Decimal
from django.conf import settings
import requests
from django.urls import reverse



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
    data = request.POST
    full_name   = (data.get("full_name") or "").strip()
    email       = (data.get("email") or "").strip()
    mobile_no   = (data.get("mobile_no") or "").strip()
    outlet_id   = data.get("outlet")
    service_ids = data.getlist("services")  # multiple checkboxes share the same name
    booking_date = data.get("booking_date")
    booking_time = data.get("booking_time")

    outlet = Outlet.objects.filter(pk=outlet_id).first()
    services = Service.objects.filter(id__in=service_ids)

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
                payment_status="pending",
            )

            BookingService.objects.bulk_create(
                [BookingService(booking=booking, service=s) for s in services]
            )

        # Redirect to payment options page
            return redirect('payment_page', booking_id=booking.id)

    except Exception as e:
        # Redirect back to homepage if something fails
        return redirect('public_home')





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


# -------------------- Payment Page --------------------
@require_http_methods(["GET"])
def payment_page(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    # Get services and prices for this booking
    booking_services = BookingService.objects.filter(booking=booking).select_related('service')
    services = []
    total = Decimal("0.00")

    for bs in booking_services:
        # Get price for service at this outlet
        sp = OutletServicePrice.objects.filter(outlet=booking.outlet, service=bs.service).first()
        price = sp.price if sp else Decimal("0.00")
        total += price
        services.append({
            "name": bs.service.name,
            "price": price 
        })

    context = {
        "wp_header_full": mark_safe(get_wp_header_full()),
        "wp_footer_full": mark_safe(get_wp_footer_full()),
        "booking": booking,
        "services": services,
        "total": total,
    }
    return render(request, "frontend/templates/appointment/payment_page.html", context)

# -------------------- Pay Cash --------------------
def pay_cash(request, booking_id):
    # print('hfdrdd')
    booking = get_object_or_404(Booking, id=booking_id)

    # Mark booking as paid via cash
    booking.payment_status = "paid"
    booking.status = "confirmed"
    booking.save()

    # Render a temporary success page with auto-redirect
    return render(request, "frontend/templates/appointment/cash_success.html", {"booking": booking})

# -------------------- Pay eSewa --------------------



def generate_esewa_signature(total_amount, transaction_uuid, product_code):
    message = f"total_amount={total_amount},transaction_uuid={transaction_uuid},product_code={product_code}"
    secret_key = settings.ESEWA_SECRET_KEY.encode("utf-8")
    signature = hmac.new(secret_key, message.encode("utf-8"), hashlib.sha256).digest()
    return base64.b64encode(signature).decode()


@require_http_methods(["POST"])
def pay_esewa(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)

    # calculate total
    booking_services = BookingService.objects.filter(booking=booking).select_related('service')
    total = Decimal("0.00")
    for bs in booking_services:
        sp = OutletServicePrice.objects.filter(outlet=booking.outlet, service=bs.service).first()
        total += sp.price if sp else Decimal("0.00")

    transaction_uuid = str(uuid.uuid4())
    product_code = settings.ESEWA_PRODUCT_CODE
    signature = generate_esewa_signature(total, transaction_uuid, product_code)

    data = {
        "amount": total,
        "tax_amount": 0,
        "total_amount": total,
        "transaction_uuid": transaction_uuid,
        "product_code": product_code,
        "product_service_charge": 0,
        "product_delivery_charge": 0,
        "success_url": request.build_absolute_uri(
         reverse("esewa_success", args=[booking.id])
),

        "failure_url": request.build_absolute_uri(f"/esewa-fail/{booking.id}/"),
        "signed_field_names": "total_amount,transaction_uuid,product_code",
        "signature": signature,
    }

    esewa_url = "https://rc-epay.esewa.com.np/api/epay/main/v2/form"

    form_html = f"""
    <form id="esewaForm" action="{esewa_url}" method="POST">
        {''.join([f'<input type="hidden" name="{k}" value="{v}"/>' for k, v in data.items()])}
    </form>
    <script>document.getElementById('esewaForm').submit();</script>
    """
    return HttpResponse(form_html)


def generate_esewa_signature(total_amount, transaction_uuid, product_code):
    message = f"total_amount={total_amount},transaction_uuid={transaction_uuid},product_code={product_code}"
    secret_key = settings.ESEWA_SECRET_KEY.encode("utf-8")
    signature = hmac.new(secret_key, message.encode("utf-8"), hashlib.sha256).digest()
    return base64.b64encode(signature).decode()



def esewa_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.payment_status = "paid"
    booking.status = "confirmed"
    booking.save()
    return redirect('public_home')  # Redirect to index.html after success


def esewa_failure(request, booking_id):
    return HttpResponse("Payment failed. Please try again.")

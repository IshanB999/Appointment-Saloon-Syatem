from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Booking
from service.models import Service
from django.db.models import Q
from django.utils.safestring import mark_safe
import json, re

def index(request):
    base_qs = Booking.objects.select_related('outlet')
    user = request.user
    if user.is_authenticated and user.groups.filter(name__iexact='Outlet Group').exists():
        if getattr(user, 'outlet_id', None):
            base_qs = base_qs.filter(outlet_id=user.outlet_id)
        else:
            base_qs = base_qs.none()

    requested_html = re.search(r'^text/html', request.META.get('HTTP_ACCEPT') or "")
    if not requested_html:
        post = request.POST
        start = int(post.get('start', 0))
        length = int(post.get('length', 25))
        search_value = (post.get('search[value]') or "").strip()

        qs = base_qs
        if search_value:
            qs = qs.filter(
                Q(full_name__icontains=search_value) |
                Q(email__icontains=search_value) |
                Q(mobile_no__icontains=search_value) |
                Q(outlet__name__icontains=search_value)
            )

        total_count = base_qs.count()
        filtered_count = qs.count()

        object_list = qs.order_by('id')[start:start+length]

        rows = []
        for b in object_list:
            rows.append({
                "id": b.id,
                "full_name": b.full_name or "",
                "email": b.email or "",
                "mobile_no": b.mobile_no or "",
                "outlet": b.outlet.name if b.outlet else "",
                "booking_date": b.booking_date.strftime("%Y-%m-%d") if b.booking_date else "",
                "booking_time": b.booking_time.strftime("%H:%M") if b.booking_time else "",
                "status": b.status or "",
            })

        payload = {
            "draw": int(post.get('draw') or 0),
            "recordsTotal": total_count,
            "recordsFiltered": filtered_count,
            "data": rows,
        }
        return HttpResponse(mark_safe(json.dumps(payload, default=str)), content_type='application/json')

    return render(request, 'booking/index.html')


def detail(request):
    booking_id = request.GET.get("id")
    if not booking_id:
        return redirect("/admin/bookings/")

    booking = get_object_or_404(Booking.objects.select_related("outlet"), pk=booking_id)
    services = Service.objects.filter(bookingservice__booking_id=booking.id).only("id", "name", "code", "gender").order_by("name").distinct()
    
    context = {
        "booking": booking,
        "services": services,
        "title": f"Booking #{booking.id}",
    }
    return render(request, "booking/detail.html", context)

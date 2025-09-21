from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import admin
from .models import Outlet  ,OutletServicePrice
from django.shortcuts import render
from .forms import OutletForm
from django.shortcuts import redirect,get_object_or_404
from querystring_parser import parser
import re
from django.db.models import Count, Q
import json
from django.utils.safestring import mark_safe
from service.models import Service
from django.contrib import messages
def index(request):
    requested_html = re.search(r'^text/html', request.META.get('HTTP_ACCEPT') or "")
    if not requested_html:
        post_dict = parser.parse(request.POST.urlencode())
        params_search_value = (post_dict.get('search') or {}).get('value', "").strip()
        try:
            param_start = int(request.POST.get('start', 0))
            param_limit = int(request.POST.get('length', 25))
        except (TypeError, ValueError):
            param_start, param_limit = 0, 25
        qs = Outlet.objects.all()
        if params_search_value:
            qs = qs.filter(
                Q(name__icontains=params_search_value) |
                Q(address__icontains=params_search_value) |
                Q(mobile__icontains=params_search_value) |
                Q(phone__icontains=params_search_value)
            )
        count = Outlet.objects.count()
        filtered_total = qs.count()
        object_list = qs.order_by('id')[param_start:param_start + param_limit]
        rows = []
        for o in object_list:
            if o.image:
                try:
                    image_url = o.image.url
                except Exception:
                    image_url = ""
            else:
                image_url = ""
            rows.append({
                "id": o.id,
                "name": o.name or "",
                "address": o.address or "",
                "mobile": o.mobile or "",
                "image": image_url,  # <-- what your JS uses
            })
        payload = {
            "draw": int(post_dict.get('draw') or 0),
            "recordsTotal": count,
            "recordsFiltered": filtered_total,
            "data": rows,
        }
        data = mark_safe(json.dumps(payload, indent=4, sort_keys=True, default=str))
        return HttpResponse(data, content_type='application/json')
    return render(request, 'outlets/index.html')

def create(request):
    return render(request, 'outlets/create.html')

def store(request):
    if request.method == 'POST':
        form = OutletForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_outlet_index')
        else:
            print("Form errors:", form.errors)
            return render(request, 'admin/outlet/create.html', {'form': form})
    else:
        form = OutletForm()
        return render(request, 'admin/outlet/create.html', {'form': form})

def edit(request):
    try:
        id = request.GET.get('id')
        outlet = Outlet.objects.get(id=id)
        return render(request, 'outlets/edit.html', {'outlet': outlet})
    except Exception as e:
        print(e)
        return redirect('admin_outlet_index')
    
def update(request):
    id = request.POST.get('id')
    outlet = get_object_or_404(Outlet, id=id)
    if request.method == 'POST':
        form = OutletForm(request.POST, request.FILES, instance=outlet)
        if form.is_valid():
            form.save()
            return redirect('admin_outlet_index')
        else:
            print("Form errors:", form.errors)
            return render(request, 'outlets/edit.html', {'form': form, 'outlet': outlet})
    else:
        return redirect('admin_outlet_index')

def delete(request):
    if request.method == 'POST':
        try:
            id = request.POST.get('id')
            outlet = get_object_or_404(Outlet, id=id)
            outlet.delete()
            response = {
                'msg': 'Deleted',
                'success': True
            }
            data = mark_safe(json.dumps(response, indent=4, sort_keys=True, default=str))
            return HttpResponse(data, content_type='application/json')
        except Exception as e:
            print("Delete error:", e)
    response = {
        'msg': 'Deleted',
        'success': False
    }
    data = mark_safe(json.dumps(response, indent=4, sort_keys=True, default=str))
    return HttpResponse(data, content_type='application/json')


def outlet_service_list(request, outlet_id):
    outlet = get_object_or_404(Outlet, id=outlet_id)
    services = Service.objects.all()

    if request.method == "POST":
        for service in services:
            price = request.POST.get(f'price_{service.id}')
            selected = request.POST.get(f'service_{service.id}') == 'on'
            if selected and price:
                OutletServicePrice.objects.update_or_create(
                    outlet=outlet,
                    service=service,
                    defaults={'price': price}
                )
            else:
                OutletServicePrice.objects.filter(outlet=outlet, service=service).delete()
        messages.success(request, "Services updated successfully for outlet.")
        return redirect("admin_outlet_index")

    # load existing service prices
    existing_prices = {}
    for osp in OutletServicePrice.objects.filter(outlet=outlet):
        existing_prices[osp.service.id] = osp.price

    context = {
        "outlet": outlet,
        "services": services,
        "existing_prices": existing_prices,
    }
    return render(request, "outlets/service_list.html", context)

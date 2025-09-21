from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from .models import Service
from .forms import ServiceForm
from outlets.models import Outlet
from system.decorators import unauthenticated_user
from querystring_parser import parser
from django.db.models import Q
import json, re
from django.utils.safestring import mark_safe

@unauthenticated_user
def index(request):
    requested_html = re.search(r'^text/html', request.META.get('HTTP_ACCEPT'))
    if not requested_html:
        post_dict = parser.parse(request.POST.urlencode())
        params_search_value = post_dict.get('search')
        param_start = int(request.POST.get('start', 0))
        param_limit = int(request.POST.get('length', 10))

        object_list = Service.objects.filter(
            Q(name__icontains=params_search_value.get('value', ''))
        ).order_by('id')[param_start:param_start + param_limit]

        count = Service.objects.count()
        filtered_total = Service.objects.filter(
            Q(name__icontains=params_search_value.get('value', ''))
        ).count()

        row = list(object_list.values('id', 'name', 'gender', 'code'))

        # Add a default outlet_id (replace with dynamic if needed)
        outlet=Outlet.objects.first()
        outlet_id=outlet.id
        for r in row:
            r['outlet_id'] = outlet_id

        context = {
            'draw': post_dict.get('draw', 1),
            'recordsTotal': count,
            'recordsFiltered': filtered_total,
            'data': row,
        }
        data = mark_safe(json.dumps(context, default=str))
        return HttpResponse(data, content_type='application/json')

    return render(request, 'service/index.html')


@unauthenticated_user
def store(request):
    try:
        pk = request.POST.get('id')
        form = ServiceForm(request.POST, request.FILES or None)
        if pk:
            service = get_object_or_404(Service, id=pk)
            form = ServiceForm(request.POST, request.FILES or None, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service saved successfully')
        else:
            messages.error(request, 'Validation error')
        return HttpResponseRedirect("/admin/services")
    except Exception as e:
        messages.error(request, f'Store Failed: {str(e)}')
        return HttpResponseRedirect("/admin/services")


def delete(request):
    if request.method == 'POST':
        try:
            id = request.POST.get('id')
            service = get_object_or_404(Service, id=id)
            service.delete()
            return JsonResponse({'success': True, 'msg': 'Deleted'})
        except Exception as e:
            return JsonResponse({'success': False, 'msg': str(e)})
    return JsonResponse({'success': False, 'msg': 'Invalid request'})




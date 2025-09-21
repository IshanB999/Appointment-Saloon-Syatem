from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from system.decorators import unauthenticated_user, allowed_users
from .forms import UserForm, UpdateUserForm, RoleForm
from .models import *
from django.db.models import Count, Q
import json
from django.utils.safestring import mark_safe
from querystring_parser import parser
import re
from django.db.models import F
from django.contrib.auth.models import Group, User, Permission, ContentType
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.contrib.auth import authenticate, update_session_auth_hash
from outlets.models import Outlet


@unauthenticated_user
@permission_required("users.view_newuser", None, True)
def index(request):
    # Get Lube DMS Dealer
    groups = Group.objects.all()
    requested_html = re.search(r'^text/html', request.META.get('HTTP_ACCEPT'))
    outlets = Outlet.objects.all()
    if not requested_html:
        post_dict = parser.parse(request.POST.urlencode())
        params_search = post_dict.get('columns')
        params_search_value = post_dict.get('search')
        param_start = int(request.POST.get('start'))
        param_limit = int(request.POST.get('length'))
        object_list = NewUser.objects.filter(is_staff=1).filter(
            Q(first_name__icontains=params_search_value.get('value')) |
            Q(last_name__icontains=params_search_value.get('value')) |
            Q(email__icontains=params_search_value.get('value')) |
            Q(username__icontains=params_search_value.get('value'))
        ).prefetch_related('groups').order_by('id').all()[param_start:param_limit+param_start]  # or any kind of queryset
        count = NewUser.objects.filter(is_staff=1).count()
        filtered_total = NewUser.objects.filter(is_staff=1).filter(
            Q(first_name__contains=params_search_value.get('value')) |
            Q(last_name__contains=params_search_value.get('value')) |
            Q(email__contains=params_search_value.get('value')) |
            Q(username__contains=params_search_value.get('value'))
        ).order_by('id').count()
        object_list.annotate(Email=F('email')).values('email')
        row = list(object_list.annotate(group=F('groups__id')).values('email', 'first_name', 'id', 'is_active',
                                                                            'is_staff',
                                                                            'is_superuser', 'last_login', 'last_name',
                                                                            'password', 'start_date', 'username',
                                                                            'groups__name', 'group', 'last_login_date', 'last_login_ip'))
        context = {
            'draw': post_dict.get('draw'),
            'recordsTotal': count,
            'recordsFiltered': filtered_total,
            'data': row,
        }
        data = mark_safe(json.dumps(context, indent=4, sort_keys=True, default=str))
        return HttpResponse(data, content_type='application/json')
    return render(request, 'system/user/index.html', {'groups': groups, 'outlets': outlets})


def check_dublicate(request):
    valid = True
    id_exist = request.POST.get('id')
    if request.POST.get('type') == 'username':
        if id_exist:
            user_exist = NewUser.objects.filter(~Q(id=id_exist), username=request.POST.get('username'))
        else:
            user_exist = NewUser.objects.filter(username=request.POST.get('username'))
        if user_exist:
            valid = False

    if request.POST.get('type') == 'email':
        if id_exist:
            user_exist = NewUser.objects.filter(~Q(id=id_exist), email=request.POST.get('email'))
        else:
            user_exist = NewUser.objects.filter(email=request.POST.get('email'))
        if user_exist:
            valid = False

    content = {
        'valid': valid
    }
    data = mark_safe(json.dumps(content, indent=4, sort_keys=True, default=str))
    return HttpResponse(data, content_type='application/json')


@unauthenticated_user
@permission_required("users.add_newuser", None, True)
def save(request):
    pk_data = request.POST.get('id')
    if pk_data:
        form_data = UpdateUserForm(request.POST)
    else:
        form_data = UserForm(request.POST)
    success = False
    msg = 'Some went wrong'
    if form_data.is_valid():
        pk_data = request.POST.get('id')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        group = request.POST.get('group')
        outlet_id = request.POST.get('outlet_id')
        other_fields = {
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'is_active': 1,
            'is_staff': 1,
            'outlet_id': outlet_id
        }
        if pk_data:
            uid = request.POST.get('id')
            if uid:
                user = NewUser.objects.get(pk=uid)
                user.username = request.POST.get('username')
                user.first_name = request.POST.get('first_name')
                user.last_name = request.POST.get('last_name')
                user.email = request.POST.get('email')
                user.outlet_id = request.POST.get('outlet_id')
                user.save(update_fields=['username', 'first_name', 'last_name', 'email', 'outlet_id'])
                if password:
                    user.set_password(password)
                    user.save()
                if group:
                    user.groups.clear()
                    group = Group.objects.get(id=group)
                    group.user_set.add(user)
            success = True
            msg = 'User updated successfully'
            messages.success(request, 'Profile Updated Successfully')
        else:
            user = NewUser.objects.create_user(username=username, password=password, **other_fields)
            if request.POST.get('group'):
                group = Group.objects.get(id=request.POST.get('group'))
                group.user_set.add(user)
            success = True
            msg = 'User added successfully'
    content = {
        'success': success,
        'msg': msg
    }
    data = mark_safe(json.dumps(content, indent=4, sort_keys=True, default=str))
    return HttpResponse(data, content_type='application/json')


@unauthenticated_user
@permission_required("users.view_newuser", None, True)
def role(request):
    requested_html = re.search(r'^text/html', request.META.get('HTTP_ACCEPT'))
    if not requested_html:
        post_dict = parser.parse(request.POST.urlencode())
        params_search = post_dict.get('columns')
        params_search_value = post_dict.get('search')
        param_start = int(request.POST.get('start'))
        param_limit = int(request.POST.get('length'))
        object_list = Group.objects.filter(
            Q(name__icontains=params_search_value.get('value'))
        ).order_by('id').all()[param_start:param_limit+param_start]  # or any kind of queryset
        count = Group.objects.count()
        filtered_total = Group.objects.filter(
            Q(name__contains=params_search_value.get('value'))
        ).order_by('id').count()
        row = list(object_list.values())
        context = {
            'draw': post_dict.get('draw'),
            'recordsTotal': count,
            'recordsFiltered': filtered_total,
            'data': row,
        }
        data = mark_safe(json.dumps(context, indent=4, sort_keys=True, default=str))
        return HttpResponse(data, content_type='application/json')
    return render(request, 'system/role/index.html')


def save_role(request):
    form_data = RoleForm(request.POST)
    success = False
    msg = 'Some went wrong'
    if form_data.is_valid():
        pk_data = request.POST.get('id')
        name = request.POST.get('name')
        if pk_data:
            query_group = Group.objects.filter(pk=pk_data)
            group = query_group[0]
            group.name = name
            group.save(update_fields=['name'])
            success = True
            msg = 'Role updated successfully'
        else:
            group = Group(name=name)
            group.save()
            success = True
            msg = 'Role added successfully'
    content = {
        'success': success,
        'msg': msg
    }
    data = mark_safe(json.dumps(content, indent=4, sort_keys=True, default=str))
    return HttpResponse(data, content_type='application/json')


@unauthenticated_user
@allowed_users(allowed_roles=['Admin'])
def assign_user_permission(request):
    user_id = request.GET.get('user_id')
    content_type = ContentType.objects.filter(id__gte=3)
    user = NewUser.objects.get(pk=user_id)
    user_permissions = Permission.objects.filter(user=user)
    rows = list(user_permissions.values('id'))
    listed = []
    for row in rows:
        listed.append(row.get('id'))
    print(listed)
    return render(request, 'system/permission/assign_user_permission.html', {'content_type': content_type,
                                                                             'user_id': user_id, 'row': listed})


@unauthenticated_user
@allowed_users(allowed_roles=['Admin'])
def assign_role_permission(request):
    role_id = request.GET.get('role_id')
    content_type = ContentType.objects.filter(id__gte=3)
    group = Group.objects.get(pk=role_id)
    group_permissions = group.permissions.all()
    rows = list(group_permissions.values('id'))
    listed = []
    for row in rows:
        listed.append(row.get('id'))
    print(listed)
    return render(request, 'system/permission/assign_role_permission.html', {'content_type': content_type,
                                                                             'role_id': role_id, 'row': listed})


@unauthenticated_user
@allowed_users(allowed_roles=['Admin'])
def save_role_permission(request):
    permissions = request.POST.getlist('permission_id[]')
    role_id = request.POST.get('role_id')
    group = Group.objects.get(pk=role_id)
    perm_array = []
    for perm in permissions:
        per = Permission.objects.get(pk=perm)
        group.permissions.add(per)
        perm_array.append(perm)

    group_permissions = group.permissions.all()
    rows = list(group_permissions.values('id'))
    listed = []
    for row in rows:
        listed.append(str(row.get('id')))

    remove_list = list(set(listed) - set(perm_array))
    remove_list = list(map(int, remove_list))
    for remove in remove_list:
        group.permissions.remove(remove)
    messages.success(request, 'Role Permission Updated Successfully')
    return HttpResponseRedirect("/admin/users/roles")


@unauthenticated_user
@allowed_users(allowed_roles=['Admin'])
def save_user_permission(request):
    permissions = request.POST.getlist('permission_id[]')
    user_id = request.POST.get('user_id')
    user = NewUser.objects.get(pk=user_id)
    user.user_permissions.clear()
    perm_array = []
    for perm in permissions:
        per = Permission.objects.get(pk=perm)
        user.user_permissions.add(per)
        perm_array.append(perm)

    messages.success(request, 'Users Permission Updated Successfully')
    return HttpResponseRedirect("/admin/users")


@unauthenticated_user
def profile(request):
    user = NewUser.objects.get(id=request.user.id)
    return render(request, 'system/user/profile.html', {'user': user})


@unauthenticated_user
def update_profile(request):
    try:
        user = NewUser.objects.get(id=request.user.id)
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()
        messages.success(request, 'Profile update successfully!!')
        return HttpResponseRedirect('/admin/users/profile')
    except Exception as e:
        messages.success(request, 'Profile update failed!!')
        return HttpResponseRedirect('/admin/users/profile')


@unauthenticated_user
def change_password(request):
    user = NewUser.objects.get(id=request.user.id)
    return render(request, 'system/user/change_password.html', {'user': user})


@unauthenticated_user
def update_change_password(request):
    try:
        user = NewUser.objects.get(id=request.user.id)
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('password')
        authenticated_user = authenticate(username=user.email, password=current_password)
        if authenticated_user is not None:
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed successfully!!')
            return HttpResponseRedirect('/admin/users/change-password')
        else:
            messages.error(request, 'Old password not correct!!')
            return HttpResponseRedirect('/admin/users/change-password')
    except Exception as e:
        messages.error(request, 'Password update failed!!')
        return HttpResponseRedirect('/admin/users/change-password')
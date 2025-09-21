from django.http import HttpResponse
from django.shortcuts import redirect, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/login')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def unauthenticated_client_check(view_func):
    def wrapper_func(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Login required!!')
            return redirect('/customer/login')
        elif request.user.is_staff:
            messages.warning(request, 'Frontend access blocked!!')
            return HttpResponseRedirect('/admin')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def check_member(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff):
            return view_func(request, *args, **kwargs)
        else:
            messages.warning(request, 'Admin panel is not accessible from student account!!')
            return HttpResponseRedirect('/')

    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles or request.user.is_superuser or request.user.is_staff:
                return view_func(request, *args, **kwargs)
            else:
                # return HttpResponse('You are not authorized to view this page')
                return render(request, 'notification_pages/not_allowed.html')

        return wrapper_func

    return decorator


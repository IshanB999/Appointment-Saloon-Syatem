from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from outlets.models import  Outlet
from .models import Employees
from .forms import EmployeeForm

User = get_user_model()

@login_required
def index(request):
    # AJAX request for DataTables
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        employees = Employees.objects.all().values(
            'id', 'first_name', 'last_name', 'gender', 'email', 'phone_number',
            'role', 'outlet__name'
        )
        # Format each row for DataTables
        data = []
        for emp in employees:
            data.append({
                'id': emp['id'],
                'full_name': f"{emp['first_name']} {emp['last_name']}",
                'gender': emp['gender'],
                'email': emp['email'],
                'phone_number': emp['phone_number'],
                'role': emp['role'],
                'outlet': emp['outlet__name'] or '',
            })
        return JsonResponse({'data': data})

    return render(request, 'employees/index.html')


@login_required
def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            # Create linked User
            user = User.objects.create_user(
                username=form.cleaned_data['email'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                password='default123',  # Default password
                is_staff=True
            )
            user.save()

            # Create Employee
            employee = form.save(commit=False)
            employee.user = user
            employee.created_by = request.user
            employee.save()

            messages.success(request, 'Employee and User created successfully!')
            return redirect('admin_employees_index')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = EmployeeForm()

    return render(request, 'employees/add_employee.html', {'form': form})


@login_required
def delete_employee(request):
    if request.method == 'POST':
        emp_id = request.POST.get('id')
        employee = get_object_or_404(Employees, id=emp_id)

        # Delete linked user
        if employee.user:
            employee.user.delete()
        employee.delete()

        return JsonResponse({'success': True, 'msg': 'Employee deleted successfully'})
    return JsonResponse({'success': False, 'msg': 'Invalid request'})

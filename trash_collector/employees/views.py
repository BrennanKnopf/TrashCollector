from re import A
from time import strftime
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

from .models import Employee
from datetime import date
import calendar
from customers.models import Customer
# Create your views here.

# TODO: Create a function for each path created in employees/urls.py. Each will need a template as well.



@login_required
def index(request):
    # The following line will get the logged-in user (if there is one) within any view function
    logged_in_user = request.user
    try:
        # This line will return the employee record of the logged-in user if one exists
        logged_in_employee = Employee.objects.get(user=logged_in_user)

        calendar_date = date.today()
        day_of_week = date.today().strftime("%A")
        local_customers = Customer.objects.filter(zip_code = logged_in_employee.zip_code)
            #figure out how to step into next step 
            # customer name is not being added to today's trash variable 
        todays_trash = local_customers.filter(weekly_pickup = day_of_week)
        non_suspended_customers = todays_trash.exclude(suspend_start__gt= calendar_date, suspend_end__lt= calendar_date)
        trash_unpicked = non_suspended_customers.exclude(date_of_last_pickup= calendar_date)
        context = {
            'logged_in_employee': logged_in_employee,
            'calendar_date': calendar_date,
            'trash_unpicked': trash_unpicked,
        }
        

        return render(request, 'employees/index.html', context)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('employees:create'))

@login_required
def create(request):
    logged_in_user = request.user
    if request.method == "POST":
        name_from_form = request.POST.get('name')
        address_from_form = request.POST.get('address')
        zip_from_form = request.POST.get('zip_code')
        new_employee = Employee(name=name_from_form, user=logged_in_user, address=address_from_form, zip_code=zip_from_form)
        new_employee.save()
        return HttpResponseRedirect(reverse('employees:index'))
    else:
        return render(request, 'employees/create.html')

@login_required
def edit_profile(request):
    logged_in_user = request.user
    logged_in_employee = Employee.objects.get(user=logged_in_user)
    if request.method == "POST":
        name_from_form = request.POST.get('name')
        address_from_form = request.POST.get('address')
        zip_from_form = request.POST.get('zip_code')
        weekly_pickup_from_form = request.POST.get('weekly')
        logged_in_employee.name = name_from_form
        logged_in_employee.address = address_from_form
        logged_in_employee.zip_code = zip_from_form
        logged_in_employee.save()
        return HttpResponseRedirect(reverse('employees:index'))
    else:
        context = {
            'logged_in_employee': logged_in_employee
        }
        return render(request, 'employees/edit_profile.html', context)




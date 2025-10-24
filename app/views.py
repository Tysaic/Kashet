from django.shortcuts import render, redirect
from django.urls import reverse
from .models import (Budget, BudgetFile)

# Create your views here.

def root_redirect(request):
    return redirect('app:index')  # Redirect to URL named 'index' in app namespace

def index (request):
    return render(request, 'index.html')

def budget(request):
    return render(request, 'app/budgets/budget.html')

def details_budget(request):
    return render(request, 'app/budgets/details_budget.html')

def add_budget(request):
    if request.method == 'GET':
        return render(request, 'app/budgets/add_budget.html')
    elif request.method == 'POST':
        return reverse('app:budget')

def bills(request):
    return render(request, 'app/bills/bills.html')

def categories_bills(request):
    return render(request, 'app/bills/bills_categories.html')

def bills_reports(request):
    return render(request, 'app/bills/bills_reports.html')

def bills_add(request):
    return render(request, 'app/bills/bills_add.html')

def departments(request):
    return render(request, 'app/departments/departments.html')

def departments_add(request):
    return render(request, 'app/departments/departments_add.html')

def roles(request):
    return render(request, 'app/roles/roles.html')

def roles_add(request):
    return render(request, 'app/roles/roles_add.html')

def roles_users(request):
    return render(request, 'app/roles/roles_users.html')

def roles_users_add(request):
    return render(request, 'app/roles/roles_users_add.html')
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from .models import (Budget, BudgetFile)
from .forms import (BudgetForm, BudgetFileForm)
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.contrib import messages

# Create your views here.

def root_redirect(request):
    return redirect('app:index')  # Redirect to URL named 'index' in app namespace

def index (request):
    return render(request, 'index.html')

class BudgetListView(ListView):
    model = Budget
    template_name = 'app/budgets/budget.html'

# def budget(request):
#     return render(request, 'app/budgets/budget.html')

def details_budget(request):
    return render(request, 'app/budgets/details_budget.html')

class BudgetCreateView(CreateView):
    model = Budget
    form_class = BudgetForm
    template_name = 'app/budgets/add_budget.html'
    # Cambiar a la lista de budgets
    success_url = reverse_lazy('app:budget')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['file_form'] = BudgetFileForm(self.request.POST, self.request.FILES)
        else:
            context['file_form'] = BudgetFileForm()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        # Guardando el formulario del modelo Budget
        response = super().form_valid(form)
        
        # Guardando los archivos asociados si es necesario
        files = self.request.FILES.getlist('file')
        for _file in files:
            BudgetFile.objects.create(budget=self.object, file=_file)
        
        messages.success(self.request, "Presupuesto creado exitosamente")

        # agregar logs aca
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al crear el presupuesto, asegurate de que el formulario este bien.")
        return super().form_invalid(form)


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
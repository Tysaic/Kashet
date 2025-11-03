from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from .models import (Budget, BudgetFile)
from .forms import (BudgetForm, BudgetFileForm)
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.contrib import messages
from django.utils.translation import gettext as translate
from django.utils.translation import gettext_lazy
import logging

logger = logging.getLogger("app")

# Create your views here.

def index (request):
    logger.info(f"User {request.user} init in index", extra={
        "user": request.user,
        "path": request.path,
        "method": request.method,
    })
    return render(request, 'index.html')

class BudgetListView(ListView):
    model = Budget
    template_name = 'app/budgets/budget_list.html'
    context_object_name = 'budgets'

    def get_queryset(self):
        return Budget.objects.all().order_by('-created_at')
# def budget(request):
#     return render(request, 'app/budgets/budget.html')

def resume_budget(request):
    return render(request, 'app/budgets/budget.html')

class BudgetCreateView(CreateView):
    model = Budget
    form_class = BudgetForm
    template_name = 'app/budgets/budget_add.html'
    # Cambiar a la lista de budgets
    success_url = reverse_lazy('app:list_budget')

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
        
        logger.info(
            f'Budget "{self.object.title}" created by {self.request.user if self.request.user else "Anom"}',
            extra={
                "user": self.request.user if self.request.user.is_authenticated else None,
                "path": self.request.path,
                "method": self.request.method,
                "extra_data": {"identifier": str(self.object.identifier)},
            }
        )

        # agregar logs aca
        return response

    def form_invalid(self, form):
        logger.exception(
            f'Error validing Budget {self.object.title} created by {self.request.user if self.request.user else "Anom"}',
            extra={
                "user": self.request.user if self.request.user.is_authenticated else None,
                "path": self.request.path,
                "method": self.request.method,
            }
        )
        return super().form_invalid(form)

class BudgetDetailView(DetailView):
    model = Budget
    template_name = "app/budgets/budget_detail.html"
    context_object_name = "budget"
    slug_field = "identifier"
    slug_url_kwarg = "identifier"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['files'] = self.object.upload_folders.all()
        return context

class BudgetUpdateView(UpdateView):
    model = Budget
    form_class = BudgetForm
    template_name = "app/budgets/budget_update.html"
    slug_field = "identifier"
    slug_url_kwarg = "identifier"

    def get_success_url(self):
        return reverse_lazy("app:detail_budget", kwargs={'identifier': self.object.identifier})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


        if self.request.POST:
            context['file_form'] = BudgetFileForm(self.request.POST)
        else:
            context['file_form'] = BudgetFileForm()
            context['files'] = self.object.upload_folders.all()
        
        return context

    def post(self, request, *args, **kwargs):

        self.object = self.get_object()
        new_files = request.FILES.getlist('file')

        for new_file in new_files:
            logger.info(
                f'{new_file} files add to Budget: "{self.object.title}" by {self.request.user if self.request.user else "Anom"}',
                extra={
                    "user": self.request.user if self.request.user.is_authenticated else None,
                    "path": self.request.path,
                    "method": self.request.method,
                    "extra_data": {"identifier": str(self.object.identifier)},
                }
            )
            BudgetFile.objects.create(budget=self.object, file=new_file)
        
        form = self.form_class(request.POST, instance=self.object)
        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.save()
            logger.info(
            f'Budget "{self.object.title}" updated by {self.request.user if self.request.user else "Anom"}',
                extra={
                    "user": self.request.user if self.request.user.is_authenticated else None,
                    "path": self.request.path,
                    "method": self.request.method,
                    "extra_data": {"identifier": str(self.object.identifier)},
                }
            )
            return redirect("app:list_budget")
        else:
            errors = []
            for field, _list in form.errors.items():
                label = form.fields[field].label if field in form.fields else field
                errors.append(label)
            logger.warning(
                f"Error trying update budget '{self.object.title}' in fields: {errors} by {self.request.user if self.request.user else "Anom"}",
                extra = {
                    "user": self.request.user if self.request.user.is_authenticated else None,
                    "path": self.request.path,
                    "method": self.request.method,
                    "extra_data": {"identifier": str(self.object.identifier)},
                }
            )
            return self.form_invalid(form)

def deleting_file_budget(request, file_id):
        
        file_to_delete = BudgetFile.objects.get(id=file_id)
        budget = file_to_delete.budget
        file_to_delete.delete()
        logger.info(
            f'Budget "{file_to_delete.file.name}" files deleted from "{budget.title}" by {request.user if request.user else "Anom"}',
            extra={
                "user": request.user if request.user.is_authenticated else None,
                "path": request.path,
                "method": request.method,
                "extra_data": {"identifier": str(budget.identifier)},
            }
        )
        return redirect("app:update_budget", identifier = budget.identifier)

class BudgetDeleteView(DeleteView):

    model = Budget
    template_name = "app/budgets/budget_delete.html"
    slug_field = "identifier"
    slug_url_kwarg = "identifier"

    def get_success_url(self):
        messages.success(self.request, f"Presupuesto {self.object.title} eliminado correctamente.")
        return reverse_lazy("app:list_budget")

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
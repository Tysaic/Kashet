from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from .models import (
    Budget, BudgetFile, Bill, BillFile,
    CategoryBill
)
from .forms import (
    BudgetForm, BudgetFileForm, BillForm, 
    BillFileForm, CategoryBillForm)
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.contrib import messages
from django.utils.translation import gettext as translate
from django.utils.translation import gettext_lazy
import logging

logger = logging.getLogger("app")

# -- INDEX --

def index (request):
    logger.info(f"User {request.user} init in index", extra={
        "user": request.user,
        "path": request.path,
        "method": request.method,
    })
    return render(request, 'index.html')

def resume_budget(request):
    return render(request, 'app/budgets/budget.html')

# ---- BUDGET ----

class BudgetListView(ListView):
    model = Budget
    template_name = 'app/budgets/budget_list.html'
    context_object_name = 'budgets'
    paginate_by = 10

    def get_queryset(self):
        return Budget.objects.all().order_by('-created_at')

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
        #response = super().form_valid(form)
        _object = form.save(commit=False)

        if _object.status.enable:
            _object.edit = False
        
        _object.save()
        
        # Guardando los archivos asociados si es necesario
        files = self.request.FILES.getlist('file')
        for _file in files:
            BudgetFile.objects.create(budget=_object, file=_file)
        
        logger.info(
            f'Budget "{_object.title}" created by {self.request.user if self.request.user else "Anom"}',
            extra={
                "user": self.request.user if self.request.user.is_authenticated else None,
                "path": self.request.path,
                "method": self.request.method,
                "extra_data": {"identifier": str(_object.identifier)},
            }
        )

        #return response
        return redirect(self.success_url)

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

    def dispatch(self, request, *args, **kwargs):

        # Block if is False to edit
        self.object = self.get_object()
        if not self.object.edit:

            logger.warning(request, f"""El presupuesto "{self.object.title} - {self.object.identifier}" 
                esta cerrado y no se puede editar, alguien intenta entrar a el
                con el usuario {request.user}"""
            )

            return redirect('app:list_budget')
    
        return super().dispatch(request, *args, **kwargs)

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

        #Uploading new files
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
        
        # Validing the form when editing
        form = self.form_class(request.POST, instance=self.object)
        if form.is_valid():
            self.object = form.save(commit=False)
            
            if self.object.status.enable:
                # Disabling Editing if the status is enable to close
                self.object.edit = False
                
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

    def dispatch(self, request, *args, **kwargs):

        # Block if is False to edit
        self.object = self.get_object()

        if not self.object.edit:

            logger.warning(request, f"""El presupuesto "{self.object.title} - {self.object.identifier}" 
                esta cerrado y no se puede eliminar, alguien intenta entrar a el
                con el usuario {request.user}"""
            )

            return redirect('app:list_budget')
    
        return super().dispatch(request, *args, **kwargs)

# ---- BILL ----

class BillListView(ListView):
    model = Bill
    template_name = 'app/bills/bills_list.html'
    context_object_name = 'bills'
    paginate_by = 10

    def get_queryset(self):
        return Bill.objects.all().order_by('-created_at')
    
class BillCreateView(CreateView):

    model = Bill
    form_class = BillForm
    template_name = 'app/bills/bills_add.html'
    success_url = reverse_lazy('app:list_bills')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['file_form'] = BillFileForm(self.request.POST, self.request.FILES)
        else:
            context['file_form'] = BillFileForm()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        # Guardando el formulario del modelo Budget
        _object = form.save(commit=False)

        if _object.status.enable:
            _object.edit = False
        
        _object.save()
        
        # Guardando los archivos asociados si es necesario
        files = self.request.FILES.getlist('file')
        for _file in files:
            BillFile.objects.create(bill=_object, file=_file)
        
        logger.info(
            f'Budget "{_object.title}" created by {self.request.user if self.request.user else "Anom"}',
            extra={
                "user": self.request.user if self.request.user.is_authenticated else None,
                "path": self.request.path,
                "method": self.request.method,
                "extra_data": {"identifier": str(_object.identifier)},
            }
        )
        return redirect(self.success_url)

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

class BillDetailView(DetailView):
    model = Bill
    template_name = "app/bills/bills_detail.html"
    context_object_name = "bill"
    slug_field = "identifier"
    slug_url_kwarg = "identifier"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['files'] = self.object.upload_folders.all()
        return context

class BillUpdateView(UpdateView):
    model = Bill
    form_class = BillForm
    template_name = "app/bills/bills_update.html"
    slug_field = "identifier"
    slug_url_kwarg = "identifier"

    def dispatch(self, request, *args, **kwargs):

        # Block if is False to edit
        self.object = self.get_object()
        if not self.object.edit:

            logger.warning(request, f"""El presupuesto "{self.object.title} - {self.object.identifier}" 
                esta cerrado y no se puede editar, alguien intenta entrar a el
                con el usuario {request.user}"""
            )

            return redirect('app:list_bills')
    
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("app:detail_bills", kwargs={'identifier': self.object.identifier})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


        if self.request.POST:
            context['file_form'] = BillFileForm(self.request.POST)
        else:
            context['file_form'] = BillFileForm()
            context['files'] = self.object.upload_folders.all()
        
        return context

    def post(self, request, *args, **kwargs):

        self.object = self.get_object()
        new_files = request.FILES.getlist('file')

        #Uploading new files
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
            BillFile.objects.create(budget=self.object, file=new_file)
        
        # Validing the form when editing
        form = self.form_class(request.POST, instance=self.object)
        if form.is_valid():
            self.object = form.save(commit=False)
            
            if self.object.status.enable:
                # Disabling Editing if the status is enable to close
                self.object.edit = False
                
            self.object.save()
            logger.info(
            f'Bill "{self.object.title}" updated by {self.request.user if self.request.user else "Anom"}',
                extra={
                    "user": self.request.user if self.request.user.is_authenticated else None,
                    "path": self.request.path,
                    "method": self.request.method,
                    "extra_data": {"identifier": str(self.object.identifier)},
                }
            )
            return redirect("app:list_bills")
        else:
            errors = []
            for field, _list in form.errors.items():
                label = form.fields[field].label if field in form.fields else field
                errors.append(label)
            logger.warning(
                f"Error trying update bill '{self.object.title}' in fields: {errors} by {self.request.user if self.request.user else "Anom"}",
                extra = {
                    "user": self.request.user if self.request.user.is_authenticated else None,
                    "path": self.request.path,
                    "method": self.request.method,
                    "extra_data": {"identifier": str(self.object.identifier)},
                }
            )
            return self.form_invalid(form)

def deleting_file_bill(request, file_id):
        
        file_to_delete = BillFile.objects.get(id=file_id)
        bill = file_to_delete.bill
        file_to_delete.delete()
        logger.info(
            f'Bill "{file_to_delete.file.name}" files deleted from "{bill.title}" by {request.user if request.user else "Anom"}',
            extra={
                "user": request.user if request.user.is_authenticated else None,
                "path": request.path,
                "method": request.method,
                "extra_data": {"identifier": str(bill.identifier)},
            }
        )
        return redirect("app:update_bill", identifier = bill.identifier)

class BillDeleteView(DeleteView):

    model = Bill
    template_name = "app/bills/bills_delete.html"
    slug_field = "identifier"
    slug_url_kwarg = "identifier"

    def get_success_url(self):
        messages.success(self.request, f"Gasto {self.object.title} eliminado correctamente.")
        return reverse_lazy("app:list_bills")

    def dispatch(self, request, *args, **kwargs):

        # Block if is False to edit
        self.object = self.get_object()

        if not self.object.edit:

            logger.warning(request, f"""El Gasto "{self.object.title} - {self.object.identifier}" 
                esta cerrado y no se puede eliminar, alguien intenta entrar a el
                con el usuario {request.user}"""
            )

            return redirect('app:list_bills')
    
        return super().dispatch(request, *args, **kwargs)
# ---- BILL CATEGORIES ----
class CategoryBillsList(ListView):
    template_name = 'app/bills/categories/bills_categories.html'
    model = CategoryBill
    context_object_name = 'categories'
    paginate_by = 10
    
    def get_queryset(self):
        return CategoryBill.objects.all().order_by('name')

class CategoryBillCreateView(CreateView):
    model = CategoryBill
    form_class = CategoryBillForm
    template_name = 'app/bills/categories/bills_categories_add.html'
    success_url = reverse_lazy('app:categories_bills')


def bills_reports(request):
    return render(request, 'app/bills/bills_reports.html')

# ---- DEPARTMENT ----

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
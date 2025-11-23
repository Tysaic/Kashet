from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from .models import (
    Budget, BudgetFile, Bill, BillFile,
    CategoryBill, Department, TypeTransaction, StatusTransaction
)
from django.db.models import Sum
from .forms import (
    BudgetForm, BudgetFileForm, BillForm, 
    BillFileForm, CategoryBillForm, DepartmentForm,
    CustomLoginForm
)
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.contrib import messages
from django.utils.translation import gettext as translate
from django.utils.translation import gettext_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
import logging

logger = logging.getLogger("app")

# -- INDEX --
@login_required
def index (request):
    logger.info(f"User {request.user} init in index", extra={
        "user": request.user,
        "path": request.path,
        "method": request.method,
    })
    return render(request, 'index.html')


@login_required
def resume_budget(request):
    user = request.user
    
    # Determinar qué departamentos puede ver el usuario
    if user.is_superuser:
        departments = Department.objects.all()
        budgets = Budget.objects.all()
        bills = Bill.objects.all()
    else:
        departments = user.departments.all()
        budgets = Budget.objects.filter(department__in=departments)
        bills = Bill.objects.filter(department__in=departments)
    
    # Calcular totales generales
    total_budgets = budgets.aggregate(total=Sum('total_mount'))['total'] or 0
    total_bills = bills.aggregate(total=Sum('total_mount'))['total'] or 0
    balance_general = total_budgets - total_bills
    
    # Calcular por departamento
    departments_summary = []
    for dept in departments:
        dept_budgets = budgets.filter(department=dept)
        dept_bills = bills.filter(department=dept)
        
        dept_total_budgets = dept_budgets.aggregate(total=Sum('total_mount'))['total'] or 0
        dept_total_bills = dept_bills.aggregate(total=Sum('total_mount'))['total'] or 0
        dept_balance = dept_total_budgets - dept_total_bills
        
        departments_summary.append({
            'department': dept,
            'total_budgets': dept_total_budgets,
            'total_bills': dept_total_bills,
            'balance': dept_balance,
            'budgets_count': dept_budgets.count(),
            'bills_count': dept_bills.count(),
        })
    
    # Calcular por tipo de transacción
    types_summary = []
    for type_trans in TypeTransaction.objects.all():
        type_budgets = budgets.filter(type=type_trans).aggregate(total=Sum('total_mount'))['total'] or 0
        type_bills = bills.filter(type=type_trans).aggregate(total=Sum('total_mount'))['total'] or 0
        
        if type_budgets > 0 or type_bills > 0:
            types_summary.append({
                'type': type_trans,
                'budgets': type_budgets,
                'bills': type_bills,
            })
    
    # Calcular por estado
    status_summary = []
    for status in StatusTransaction.objects.all():
        status_budgets = budgets.filter(status=status).aggregate(total=Sum('total_mount'))['total'] or 0
        status_bills = bills.filter(status=status).aggregate(total=Sum('total_mount'))['total'] or 0
        status_count_budgets = budgets.filter(status=status).count()
        status_count_bills = bills.filter(status=status).count()
        
        if status_budgets > 0 or status_bills > 0:
            status_summary.append({
                'status': status,
                'budgets': status_budgets,
                'bills': status_bills,
                'budgets_count': status_count_budgets,
                'bills_count': status_count_bills,
            })
    
    # Últimos registros
    recent_budgets = budgets.order_by('-created_at')[:5]
    recent_bills = bills.order_by('-created_at')[:5]
    
    context = {
        'total_budgets': total_budgets,
        'total_bills': total_bills,
        'balance_general': balance_general,
        'departments_summary': departments_summary,
        'types_summary': types_summary,
        'status_summary': status_summary,
        'recent_budgets': recent_budgets,
        'recent_bills': recent_bills,
        'budgets_count': budgets.count(),
        'bills_count': bills.count(),
        'departments_count': departments.count(),
    }
    
    logger.info(
        f"User {user} viewed budget resume",
        extra={
            "user": user,
            "path": request.path,
            "method": request.method,
        }
    )
    
    return render(request, 'app/budgets/budget.html', context)

# -- LOGIN & LOGOUT --
def login_view(request):

    if request.user.is_authenticated:
        return redirect('app:index')

    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            email_username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email_username, password=password)

            if user is not None:
                login(request, user)
                logger.info(f"User {email_username} is loggin.")
                return redirect('app:index')
    else:
        form = CustomLoginForm()
    
    return render(request, 'auth/login.html', { 'form' : form })

@login_required
def logout_view(request):
    logger.info(f"User {request.user} is logout")
    logout(request)
    return redirect('app:login')
    


# ---- BUDGET ----

class BudgetListView(LoginRequiredMixin, ListView):
    model = Budget
    template_name = 'app/budgets/budget_list.html'
    context_object_name = 'budgets'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Budget.objects.all().order_by('-created_at')
        else:
            return Budget.objects.filter(
                department__in= user.departments.all()
            ).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logger.info(
            f"User {self.request.user} access budget list",
            extra={
                "user": self.request.user,
                "path": self.request.path,
                "method": self.request.method
            }
        )
        return context

class BudgetCreateView(LoginRequiredMixin, CreateView):
    model = Budget
    form_class = BudgetForm
    template_name = 'app/budgets/budget_add.html'
    # Cambiar a la lista de budgets
    success_url = reverse_lazy('app:list_budget')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

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

class BudgetDetailView(LoginRequiredMixin, DetailView):
    model = Budget
    template_name = "app/budgets/budget_detail.html"
    context_object_name = "budget"
    slug_field = "identifier"
    slug_url_kwarg = "identifier"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['files'] = self.object.upload_folders.all()
        return context

class BudgetUpdateView(LoginRequiredMixin, UpdateView):
    model = Budget
    form_class = BudgetForm
    template_name = "app/budgets/budget_update.html"
    slug_field = "identifier"
    slug_url_kwarg = "identifier"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
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
        form = self.form_class(request.POST, instance=self.object, user=request.user)
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

class BudgetDeleteView(LoginRequiredMixin, DeleteView):

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
        elif self.object.bills.exists():

            logger.warning(request, f"""El presupuesto "{self.object.title} - {self.object.identifier}" 
                tiene gastos asociados y no se puede eliminar, alguien intenta entrar a el
                con el usuario {request.user}""")
            return redirect('app:list_budget')
    
        return super().dispatch(request, *args, **kwargs)

# ---- BILL ----
class BillListView(LoginRequiredMixin, ListView):
    model = Bill
    template_name = 'app/bills/bills_list.html'
    context_object_name = 'bills'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            queryset = Bill.objects.all().order_by('-created_at')
        else:
            queryset = Bill.objects.filter(
                department__in=user.departments.all()
            ).order_by('-created_at')
        
        category_id = self.request.GET.get('category', '0')
        if category_id and category_id != '0':
            if category_id == 'NULL':
                queryset = queryset.filter(category__isnull=True)
            elif category_id != '':  # Solo filtrar si no es vacío
                queryset = queryset.filter(category_id=category_id)
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = CategoryBill.objects.all().order_by('id')
        context['selected_category'] = self.request.GET.get('category', '0')
        logger.info(
            f"User {self.request.user} access bill list",
            extra={
                "user": self.request.user,
                "path": self.request.path,
                "method": self.request.method
            }
        )
        return context
        

class BillCreateView(LoginRequiredMixin, CreateView):

    model = Bill
    form_class = BillForm
    template_name = 'app/bills/bills_add.html'
    success_url = reverse_lazy('app:list_bills')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
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

class BillDetailView(LoginRequiredMixin, DetailView):
    model = Bill
    template_name = "app/bills/bills_detail.html"
    context_object_name = "bill"
    slug_field = "identifier"
    slug_url_kwarg = "identifier"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['files'] = self.object.upload_folders.all()
        return context

class BillUpdateView(LoginRequiredMixin, UpdateView):
    model = Bill
    form_class = BillForm
    template_name = "app/bills/bills_update.html"
    slug_field = "identifier"
    slug_url_kwarg = "identifier"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

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
                f'{new_file} files add to Bill: "{self.object.title}" by {self.request.user if self.request.user else "Anom"}',
                extra={
                    "user": self.request.user if self.request.user.is_authenticated else None,
                    "path": self.request.path,
                    "method": self.request.method,
                    "extra_data": {"identifier": str(self.object.identifier)},
                }
            )
            BillFile.objects.create(bill=self.object, file=new_file)
        
        # Validing the form when editing
        form = self.form_class(request.POST, instance=self.object, user=request.user)
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

class BillDeleteView(LoginRequiredMixin, DeleteView):

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
class CategoryBillsList(LoginRequiredMixin, ListView):
    template_name = 'app/bills/categories/bills_categories.html'
    model = CategoryBill
    context_object_name = 'categories'
    paginate_by = 10
    
    def get_queryset(self):
        return CategoryBill.objects.all().order_by('name')

class CategoryBillCreateView(LoginRequiredMixin, CreateView):
    model = CategoryBill
    form_class = CategoryBillForm
    template_name = 'app/bills/categories/bills_categories_add.html'
    success_url = reverse_lazy('app:categories_bills')

class CategoryBillUpdateView(LoginRequiredMixin, UpdateView):
    model = CategoryBill
    form_class = CategoryBillForm
    template_name = 'app/bills/categories/bills_categories_update.html'
    success_url = reverse_lazy('app:categories_bills')
    slug_field = 'id'
    slug_url_kwarg = 'id'

class CategoryBillDeleteView(LoginRequiredMixin, DeleteView):
    model = CategoryBill
    context_object_name = 'category'
    template_name = 'app/bills/categories/bills_categories_delete.html'
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def get_success_url(self):
        _object = self.get_object()
        logger.info(translate(f"Categoria siendo eliminara '{_object.name}'"))
        return reverse_lazy("app:categories_bills")
    
    def dispatch(self, request, *args, **kwargs):
        _object = self.get_object()

        if _object.has_bills or _object.has_children:
            logging.warning(request, f"""
            La Categoria '{_object.name}' no se puede eliminar debido a que tiene gastos asignados,
            o es padre de subcategorias.
            """)
            return redirect("app:categories_bills")
        
        return super().dispatch(request, *args, **kwargs)

@login_required
def bills_reports(request):
    return render(request, 'app/bills/bills_reports.html')

# ---- DEPARTMENT ----

class DepartmentListView(LoginRequiredMixin, ListView):
    model = Department
    template_name = 'app/departments/departments.html'
    context_object_name = 'departments'
    paginate_by = 10

    def get_queryset(self):
        query_set = super().get_queryset()
        user = self.request.user

        if user.is_superuser:
            return query_set
        
        #return Budget.objects.all().order_by('-created_at')
        return user.departments.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['total_budgets'] = Budget.objects.count()
        context['total_bills'] = Bill.objects.count()

        return context

class DepartmentDetailsView(LoginRequiredMixin, DetailView):

    model = Department
    template_name = 'app/departments/departments_details.html'
    context_object_name = 'department'
    slug_field = 'id'
    slug_url_kwarg = 'id'

class DepartmentCreateView(LoginRequiredMixin, CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'app/departments/departments_add.html'
    success_url = reverse_lazy('app:list_departments')

class DepartmentUpdateView(LoginRequiredMixin, UpdateView):

    model = Department
    form_class = DepartmentForm
    template_name = 'app/departments/departments_update.html'
    success_url = reverse_lazy('app:list_departments')
    slug_field = 'id'
    slug_url_kwarg = 'id'
    
class DepartmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Department
    context_object_name = 'department'
    template_name = 'app/departments/departments_delete.html'
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def get_success_url(self):
        _object = self.get_object()
        logger.info(translate(f"Departamento siendo eliminara '{_object.name}'"))
        return reverse_lazy("app:list_departments")
    
    def dispatch(self, request, *args, **kwargs):
        _object = self.get_object()

        if _object.has_budget or _object.has_bills:
            logging.warning(request, f"""
            Departamento '{_object.name}' no se puede eliminar debido a que tiene gastos asignados,
            y/o presupuesto asignado.
            """)
            return redirect("app:list_departments")
        
        return super().dispatch(request, *args, **kwargs)

#def departments_add(request):
#    return render(request, 'app/departments/departments_add.html')

@login_required
def roles(request):
    return render(request, 'app/roles/roles.html')

@login_required
def roles_add(request):
    return render(request, 'app/roles/roles_add.html')

@login_required
def roles_users(request):
    return render(request, 'app/roles/roles_users.html')

@login_required
def roles_users_add(request):
    return render(request, 'app/roles/roles_users_add.html')
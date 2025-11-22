from django import forms
from .models import (Budget, BudgetFile, Bill, BillFile, CategoryBill, Department, CustomUser)
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, ReadOnlyPasswordHashField
from django.utils.formats import number_format
from django.utils.translation import gettext_lazy as translate
from .models import StatusTransaction
from datetime import date

class BudgetForm(forms.ModelForm):

    class Meta:
        model = Budget
        fields = [
            'title',
            'description',
            'type',
            'status',
            'department',
            'total_mount',
            'currency',
            'due_date',
            'set_date',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': translate('Ingrese aca el presupuesto')}),
            'set_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'value': date.today().strftime('%Y-%m-%d')}, format='%Y-%m-%d'),
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'value': date.today().strftime('%Y-%m-%d')}, format='%Y-%m-%d'),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': translate('Descripcion detallada del presupuesto ...')}),
            'total_mount': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_total_mount','placeholder': '0.00'}),
            'currency': forms.Select(attrs={'class': 'form-select', 'placeholder': translate('Ingrese la moneda.')}),
            'type': forms.Select(attrs={'class': 'form-select', 'placeholder': translate('Ingrese tipo de gasto.')}),
            'status': forms.Select(attrs={'class': 'form-select', 'placeholder': translate('Estado del presupuesto')}),
            'department': forms.Select(attrs={'class': 'form-select', 'placeholder': translate('Ingrese aca el departamento')}),
        }
        labels = {
            'title': translate('Titulo del Presupuesto'),
            'description': translate('Descripcion'),
            'type': translate('Tipo de Transacción'),
            'status': translate('Estado del presupuesto.'),
            'department': translate('Departamento'),
            'total_mount': translate('Monto Total'),
            'currency': translate('Moneda'),
            'due_date': translate('Fecha de tope de Presupuesto'),
            'set_date': translate('Fecha de inicio de Presupuesto'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['due_date'].input_formats = ['%Y-%m-%d'] 
        # Just new forms on budget_add
        if not self.instance.pk:
            default_status = StatusTransaction.objects.filter(name__icontains=translate('En Proceso')).first()
            if default_status:
                self.fields['status'].initial = default_status.id
            else:
                self.fields['status'].initial = StatusTransaction.objects.first().id


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class BudgetFileForm(forms.ModelForm):

    class Meta:
        model = BudgetFile
        fields = ['file']
        widgets = {
            'file' : MultipleFileInput(attrs={'class': 'form-control', 'multiple': True}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file'].required = False
    

class BillForm(forms.ModelForm):
    
    class Meta:

        model = Bill
        fields = [
            'title',
            'description',
            'total_mount',
            'currency',
            'due_date',
            'budget',
            'type',
            'status',
            'department',
            'category',
        ]

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': translate('Ingrese aca el presupuesto')}),
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'value': date.today().strftime('%Y-%m-%d')}, format='%Y-%m-%d'),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': translate('Descripcion detallada del presupuesto ...')}),
            'total_mount': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_total_mount','placeholder': '0.00'}),
            'currency': forms.Select(attrs={'class': 'form-select', 'placeholder': translate('Ingrese la moneda.')}),
            'type': forms.Select(attrs={'class': 'form-select', 'placeholder': translate('Ingrese tipo de gasto.')}),
            'status': forms.Select(attrs={'class': 'form-select', 'placeholder': translate('Estado del presupuesto')}),
            'department': forms.Select(attrs={'class': 'form-select', 'placeholder': translate('Ingrese aca el departamento')}),
            'budget': forms.Select(attrs={'class': 'form-select', 'placeholder': translate('Ingrese aca el presupuesto')}),
            'category': forms.Select(attrs={'class': 'form-select', 'placeholder': translate('Ingrese la categoria de gasto.')})
        }
        labels = {
            'title': translate('Titulo del Presupuesto'),
            'description': translate('Descripcion'),
            'type': translate('Tipo de Transacción'),
            'status': translate('Estado del presupuesto.'),
            'department': translate('Departamento'),
            'total_mount': translate('Monto Total'),
            'currency': translate('Moneda'),
            'due_date': translate('Fecha de tope de gasto'),
            'budget': translate('Presupuesto'),
            'category': translate('Categoria'),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['due_date'].input_formats = ['%Y-%m-%d'] 
        # Just new forms on budget_add
        if not self.instance.pk:
            default_status = StatusTransaction.objects.filter(name__icontains=translate('En Proceso')).first()
            if default_status:
                self.fields['status'].initial = default_status.id
            else:
                self.fields['status'].initial = StatusTransaction.objects.first().id


class BillFileForm(forms.ModelForm):

    class Meta:
        model = BillFile
        fields = ['file']
        widgets = {
            'file' : MultipleFileInput(attrs={'class': 'form-control', 'multiple': True}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file'].required = False

class CategoryBillForm(forms.ModelForm):

    class Meta:
        model = CategoryBill
        fields = ['name', 'description', 'parent']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': translate('Ingrese el nombre de la categoria')}),
            'description': forms.Textarea(attrs={'rows':4, 'class': 'form-control', 'placeholder': translate('Descripcion detallada de la categoria ...')}),
            'parent': forms.Select(attrs={'class': 'form-select', 'placeholder': translate('Selecciones una categoria padre si aplica.')})
        }

        labels = {
            'name': translate('Nombre de la categoria'),
            'description': translate('Descripcion'),
            'parent': translate('Categoria Padre (Opcional)'),
        }

class DepartmentForm(forms.ModelForm):

    class Meta:

        model = Department
        fields = [
            'name',
            'description',
            'location',
            'phone',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': translate('Ingrese el nombre del Departamento')}),
            'description': forms.Textarea(attrs={'rows':4, 'class': 'form-control', 'placeholder': translate('Descripcion detallada del departamento ...')}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': translate('Ingrese su Domicilio')}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': translate('Ingrese su Telefono')}),
        }
        labels = {
            'name': translate('Nombre del Departamento'),
            'description': translate('Descripción'),
            'location': translate('Domicilio'),
            'phone': translate('Telefono'),
        }


# ------ Login Site ------
class CustomLoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget = forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email',
            'autofocus': True
        })
    )
    password = forms.CharField(
        widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': translate('Contraseña'),
        })
    )

class CustomUserCreationForm(forms.ModelForm):
    
    first_password = forms.CharField(
        label = 'password',
        widget = forms.PasswordInput()
    )
    second_password = forms.CharField(
        label = 'Confirm password',
        widget = forms.PasswordInput()
    )

    class Meta:

        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name', 'is_active', 'is_staff', 'phone', 'departments')
    
    def clean(self):
        cleaned_data = super().clean()
        first_password = cleaned_data.get("first_password")
        second_password = cleaned_data.get("second_password")

        if first_password and second_password and first_password != second_password:
            raise forms.ValidationError("The password doesn't match!")
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["first_password"])

        if commit:
            user.save()
            self.save_m2m()
        return user
    

class CustomUserChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField(
        label='password',
        help_text = (
            "The passwords is stored hashed"
            "Could change the password using specific forms."
        )
    )

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "phone",
            "departments",
            "password",
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions",
        )

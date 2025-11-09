from django import forms
from .models import (Budget, BudgetFile, Bill, BillFile)
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
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': translate('Ingrese aca el presupuesto')}),
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'value': date.today().strftime('%Y-%m-%d')}, format='%Y-%m-%d'),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': translate('Descripcion detallada del presupuesto ...')}),
            'total_mount': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_total_mount','placeholder': '0.00'}),
            'currency': forms.Select(attrs={'class': 'form-select'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
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
            'due_date': translate('Fecha de tope de gasto'),
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
            'department'
        ]

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': translate('Ingrese aca el presupuesto')}),
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'value': date.today().strftime('%Y-%m-%d')}, format='%Y-%m-%d'),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': translate('Descripcion detallada del presupuesto ...')}),
            'total_mount': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_total_mount','placeholder': '0.00'}),
            'currency': forms.Select(attrs={'class': 'form-select'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select', 'placeholder': translate('Estado del presupuesto')}),
            'department': forms.Select(attrs={'class': 'form-select', 'placeholder': translate('Ingrese aca el departamento')}),
            'budget': forms.Select(attrs={'class': 'form-select', 'placeholder': translate('Ingrese aca el presupuesto')})
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
            'budget': translate('Presupuesto')
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
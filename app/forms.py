from django import forms
from .models import Budget, BudgetFile

class BudgetForm(forms.ModelForm):

    class Meta:
        model = Budget
        fields = [
            'title',
            'description',
            'type',
            'department',
            'total_mount',
            'currency',
            'due_date',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese aca el presupuesto'}),
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Descripcion detallada del presupuesto ...'}),
            'total_mount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00', 'step': '10000'}),
            'currency': forms.Select(attrs={'class': 'form-select'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'department': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Ingrese aca el departamento'}),
        }
        labels = {
            'title': 'Titulo del Presupuesto',
            'description': 'Descripcion',
            'type': 'Tipo de Presupuesto',
            'department': 'Departamento',
            'total_mount': 'Monto Total',
            'currency': 'Moneda',
            'due_date': 'Fecha de tope de gasto',
        }

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class BudgetFileForm(forms.ModelForm):

    class Meta:
        model = BudgetFile
        fields = ['file']
        widgets = {
            'file' : MultipleFileInput(attrs={'class': 'form-control', 'multiple': True}),
        }
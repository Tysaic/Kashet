from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
import uuid
import os

def budget_upload_path(instance, filename):
    return os.path.join('budgets', str(instance.budget.identifier), filename)

class Budget(models.Model):
    CURRENCIES = (
        ('CLP', 'Chilean Peso ($)'),
        ('USD', 'US Dollar ($)'),
        ('EUR', 'Euro (€)')
    )
    TYPE_OF_BUDGET = (
        ('1', 'Transferencia Bancaria'),
        ('2', 'Efectivo'),
        ('3', 'Orden de Pago'),
        ('4', 'Debito/Credito')
    )
    title = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    total_mount = models.DecimalField(max_digits=24, decimal_places=0, validators=[MinValueValidator(0.01, message="Monto debe ser positivo.")])
    identifier = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    currency = models.CharField(max_length=3, choices=CURRENCIES, default=CURRENCIES[0][0])
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=1, choices=TYPE_OF_BUDGET, default=TYPE_OF_BUDGET[0][0])
    department = models.ForeignKey(
        'Department', 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL, 
        related_name='budgets'
    )
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.description} - ({self.total_mount} {self.currency})"
    

class BudgetFile(models.Model):
    budget = models.ForeignKey(Budget, related_name="upload_folders", on_delete=models.CASCADE)
    file = models.FileField(upload_to=budget_upload_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name

# class TypeTransaction
# class Departments

class Department(models.Model):

    name = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



class ActivityLog(models.Model):
    LEVELS = [
        ('INFO', 'Info'),
        ('WARNING', 'Warning'),
        ('ERROR', 'Error'),
    ]

    #user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    level = models.CharField(max_length=10, choices=LEVELS, default='INFO')
    action = models.CharField(max_length=255)
    method = models.CharField(max_length=10, null=True, blank=True)
    path = models.CharField(max_length=255, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    extra_data = models.JSONField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        #return f'[{self.timestamp: %Y-%m-%d %H:%M}] {self.user or "System"} - self.action'
        return f'[{self.timestamp: %Y-%m-%d %H:%M}] {"System"} - self.action'


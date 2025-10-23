from django.db import models
import uuid
import os

def budget_upload_path(instance, filename):
    return os.path.join('budgets', str(instance.budget.identifier), filename)

class Budget(models.Model):
    CURRENCIES = [
        ('CLP', 'Chilean Peso ($)'),
        ('USD', 'US Dollar ($)'),
        ('EUR', 'Euro (€)')
    ]
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    total_mount = models.DecimalField(max_digits=24, decimal_places=2)
    identifier = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    currency = models.CharField(max_length=3, choices=CURRENCIES, default=CURRENCIES[0][0])
    created_at = models.DateField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    enable = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.description} - ({self.total_mount} {self.currency})"
    

class BudgetFile(models.Model):
    budget = models.ForeignKey(Budget, related_name="upload_folders", on_delete=models.CASCADE)
    file = models.FileField(upload_to=budget_upload_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name



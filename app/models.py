from django.db import models
from django.db.models import Sum
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as translate
from django.utils import timezone
import uuid
import os


"""---------BUDGET---------"""

def returning_title_to_bill_and_budget(set_date, due_date, department, title, total_mount, currency):
    MONTHS = [
        translate('Enero'), translate('Febrero'), translate('Marzo'),
        translate('Abril'), translate('Mayo'), translate('Junio'),
        translate('Julio'), translate('Agosto'), translate('septiembre'),
        translate('Octubre'), translate('Noviembre'), translate('Diciembre'),
    ]
    month_due_date = MONTHS[ due_date.month -1 ]
    month_set_date = MONTHS[ set_date.month -1 ]
    title_to_str = f"{month_set_date}/{month_due_date} - {department} - {title} - ({total_mount} {currency})"
    return  title_to_str

def budget_upload_path(instance, filename):
    return os.path.join('budgets', str(instance.budget.identifier), filename)

class Budget(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    total_mount = models.DecimalField(max_digits=24, decimal_places=0, validators=[MinValueValidator(0.01, message="Monto debe ser positivo.")])
    identifier = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    set_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    due_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    edit = models.BooleanField(default=True)
    status = models.ForeignKey(
        'StatusTransaction',
        on_delete = models.PROTECT,
        null=False,
        blank=False,
        related_name='budgets',
    )
    type = models.ForeignKey(
        'TypeTransaction', 
        null=False, 
        blank=False, 
        on_delete=models.PROTECT,
        related_name='budgets'
    )
    currency = models.ForeignKey(
        'Currency', 
        null=False, 
        blank=False, 
        on_delete=models.PROTECT,
        related_name='budgets'
    )
    
    department = models.ForeignKey(
        'Department', 
        null=False, 
        blank=False, 
        on_delete=models.PROTECT, 
        related_name='budgets'
    )
    class Meta:
        ordering = ['-created_at']
        verbose_name = translate("budget")
        verbose_name_plural = translate("budgets")
    
    def __str__(self):
        return returning_title_to_bill_and_budget(
            self.set_date, self.due_date, self.department, 
            self.title,self.total_mount, self.currency
        )
    
    @property
    def has_bills(self):
        return self.bills.exists()


class BudgetFile(models.Model):
    budget = models.ForeignKey(Budget, related_name="upload_folders", on_delete=models.CASCADE)
    file = models.FileField(upload_to=budget_upload_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = translate("budget_file")
        verbose_name_plural = translate("budget_files")

    def __str__(self):
        return self.file.name

"""---------BUDGET---------"""


"""---------BILLS---------"""
def bill_upload_path(instance, filename):
    return os.path.join('bills', str(instance.bill.identifier), filename)

class Bill(models.Model):

    title = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    total_mount = models.DecimalField(max_digits=24, decimal_places=0, validators=[
        MinValueValidator(0.01, message="Monto debe ser positivo.")]
    )
    identifier = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    due_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    edit = models.BooleanField(default=True)

    budget = models.ForeignKey(
        'Budget',
        on_delete=models.PROTECT,
        related_name='bills',
        null=False,
        blank=False
    )
    status = models.ForeignKey(
        'StatusTransaction',
        on_delete = models.PROTECT,
        null=False,
        blank=False,
        related_name='bills',
    )
    type = models.ForeignKey(
        'TypeTransaction', 
        null=False, 
        blank=False, 
        on_delete=models.PROTECT,
        related_name='bills',
    )
    currency = models.ForeignKey(
        'Currency', 
        null=False, 
        blank=False, 
        on_delete=models.PROTECT,
        related_name='bills',
    )

    department = models.ForeignKey(
        'Department', 
        null=False, 
        blank=False, 
        on_delete=models.PROTECT, 
        related_name='bills'
    )

    category = models.ForeignKey(
        'CategoryBill',
        on_delete=models.PROTECT,
        related_name='bills',
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = translate("bill")
        verbose_name_plural = translate("bills")
    
    def __str__(self):
        return returning_title_to_bill_and_budget(
            self.set_date, self.due_date, self.department, 
            self.title,self.total_mount, self.currency
        )

    
class BillFile(models.Model):
    bill = models.ForeignKey(Bill, related_name="upload_folders", on_delete=models.CASCADE)
    file = models.FileField(upload_to=bill_upload_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = translate("bill_file")
        verbose_name_plural = translate("bill_files")

    def __str__(self):
        return self.file.name
"""---------BILLS---------"""

"""---------CATEGORIES BILLS---------"""
class CategoryBill(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    parent = models.ForeignKey(
        'self',
        on_delete = models.SET_NULL,
        null=True,
        blank=True,
        related_name = 'subcategories',
    )

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} -> {self.name}"
        return self.name
    
    class Meta:
        verbose_name = translate("category_bill")
        verbose_name_plural = translate("category_bills")
        ordering = ['name']
    
    @property
    def is_subcategory(self):
        if self.parent:
            return True
        return False
    
    @property
    def get_all_subcategories(self):
        sub_categories = list(self.subcategories.all())

        for subcat in sub_categories:
            sub_categories.extend(subcat.get_all_subcategories)
        
        return sub_categories
    
    @property
    def get_bills_count(self):
        return self.bills.count()
    
    @property
    def has_bills(self):
        return self.bills.exists()
    
    @property
    def has_children(self):
        return self.subcategories.exists()


    
"""---------CATEGORIES BILLS---------"""

"""---------DEPARTMENTS---------"""
class Department(models.Model):

    name = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = translate("department")
        verbose_name_plural = translate("departments")        

    def __str__(self):
        return self.name
    
    # Method to attribute of just reading.
    # ca access with department.objects.get(id=1).get_total_budgets
    @property
    def get_total_budgets(self):
        return self.budgets.aggregate(total = Sum('total_mount'))['total'] or 0

    @property
    def get_total_bills(self):
        return self.bills.aggregate(total = Sum('total_mount'))['total'] or 0
    
    @property
    def balance(self):
        return self.get_total_budgets + self.get_total_bills
    
    @property
    def get_budget_count(self):
        return self.budgets.count()
    
    @property
    def get_bills_count(self):
        return self.bills.count()
"""---------DEPARTMENTS---------"""

"""---------CURRENCY---------"""
class Currency(models.Model):
    name = models.CharField(max_length=32)
    code = models.CharField(max_length=3, unique=True)
    symbol = models.CharField(max_length=3)

    class Meta:
        verbose_name = translate("currency")
        verbose_name_plural = translate("currencies")
    
    def __str__(self):
        return f"{self.name} - {self.code} - {self.symbol}"
"""---------CURRENCY---------"""

"""---------TYPETRANSACTION---------"""
class TypeTransaction(models.Model):
    name = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = translate("type_transaction")
        verbose_name_plural = translate("type_transactions")
    
    def __str__(self):
        return self.name
"""---------TYPETRANSACTION---------"""

"""---------STATUS_TRANSACTION---------"""
class StatusTransaction(models.Model):
    name = models.CharField(max_length=32)
    enable = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = translate("status_transaction")
        verbose_name_plural = translate("status_transactions")

    def __str__(self):
        return self.name
"""---------STATUS_TRANSACTION---------"""

"""---------ACTIVITY_LOG---------"""
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
        verbose_name = translate("activity_log")
        verbose_name_plural = translate("activity_logs")    

    def __str__(self):
        #return f'[{self.timestamp: %Y-%m-%d %H:%M}] {self.user or "System"} - self.action'
        return f'[{self.timestamp: %Y-%m-%d %H:%M}] {"System"} - self.action'

"""---------ACTIVITY_LOG---------"""


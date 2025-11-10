from django.contrib import admin
from .models import (
    Budget, BudgetFile, Department, 
    Bill, BillFile, Currency, CategoryBill,
    TypeTransaction, StatusTransaction ,ActivityLog)


class BudgetFileInLine(admin.TabularInline):
    model = BudgetFile
    extra = 1

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'total_mount', 'edit',
        'currency', 'created_at', 
         'due_date','type', 'department',
        )
    search_fields = ('title', 'department')
    inlines = [BudgetFileInLine]

@admin.register(BudgetFile)
class BudgetFileAdmin(admin.ModelAdmin):
    list_display= ('budget', 'file')

@admin.register(StatusTransaction)
class StatusTransactionAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')


class BillFileInLine(admin.TabularInline):
    model = BillFile
    extra = 1

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'total_mount', 
        'currency', 'created_at', 
         'due_date','type', 'department'
        )
    search_fields = ('title', 'department')
    inlines = [BillFileInLine]
    
@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'symbol')

@admin.register(TypeTransaction)
class TypeTransactionAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')

@admin.register(Department)
class DepartmentsAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "level", "action", "method", "path", "ip_address") #"user",)
    list_filter = ("level", "timestamp")#"user",)
    search_fields = ("action", "path",) #"user__username")
    ordering = ("-timestamp",)

@admin.register(CategoryBill)
class CategoryBillAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
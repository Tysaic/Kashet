from django.contrib import admin
from .models import (Budget, BudgetFile, Department)


class BudgetFileInLine(admin.TabularInline):
    model = BudgetFile
    extra = 1

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'total_mount', 
        'currency', 'created_at', 
         'due_date','type', 'department'
        )
    search_fields = ('title', 'department')
    inlines = [BudgetFileInLine]

@admin.register(BudgetFile)
class BudgetFileAdmin(admin.ModelAdmin):
    list_display= ('budget', 'file')
# Register your models here.

@admin.register(Department)
class DepartmentsAdmin(admin.ModelAdmin):
    list_display = ('name',)

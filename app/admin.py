from django.contrib import admin
from .models import (Budget, BudgetFile)

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'description', 'total_mount', 
        'identifier', 'currency', 'created_at', 
         'type', 'department'
        )
    search_fields = ('title', 'department')


@admin.register(BudgetFile)
class BudgetFileAdmin(admin.ModelAdmin):
    list_display= ('budget', 'file')
# Register your models here.

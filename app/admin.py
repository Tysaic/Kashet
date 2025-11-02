from django.contrib import admin
from .models import (Budget, BudgetFile, Department, ActivityLog)


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

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "level", "action", "method", "path", "ip_address") #"user",)
    list_filter = ("level", "timestamp")#"user",)
    search_fields = ("action", "path",) #"user__username")
    ordering = ("-timestamp",)
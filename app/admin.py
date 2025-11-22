from django.contrib import admin
from .models import (
    Budget, BudgetFile, Department, 
    Bill, BillFile, Currency, CategoryBill,
    TypeTransaction, StatusTransaction ,ActivityLog,
    CustomUser
)
<<<<<<< HEAD
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
=======
from django.contrib.auth.admin import UserAdmin
>>>>>>> 5e240813578a946e091ea2cf7a49e6d7bed41871

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
    list_display = ('name', 'description', 'phone', 'location')
    search_fields = ('name', 'phone', 'location')

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "level", "action", "method", "path", "ip_address") #"user",)
    list_filter = ("level", "timestamp")#"user",)
    search_fields = ("action", "path",) #"user__username")
    ordering = ("-timestamp",)

@admin.register(CategoryBill)
class CategoryBillAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm # To Edit
    add_form = CustomUserCreationForm

    list_display = ("email", "username", "is_staff", "is_active",)
    list_filter = ("is_staff", "is_superuser", "is_active", "departments")
    search_fields = ("email", "username", "first_name", "last_name")
    #ordering = ("-date_joined",)

    filter_horizontal = ("departments", "groups", "user_permissions")

    # Fieldsets para editar usuarios existentes
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {
            "fields": ("username", "first_name", "last_name", "phone", "departments")
        }),
        ("Permissions", {
            "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")
        }),
        ("Important Dates", {
            "fields": ("last_login",)
        }),
    )

    # Fieldsets para crear nuevos usuarios
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email",
                "username",
                "first_name",
                "last_name",
                "phone",
                "departments",
                "first_password",
                "second_password",
                "is_staff",
                "is_active"
            )
        }),
    )

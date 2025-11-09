from . import views
from django.urls import path

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('resume_budgets/', views.resume_budget, name='resume_budgets'),
    path('list_budget/', views.BudgetListView.as_view(), name='list_budget'),
    path('add_budget/', views.BudgetCreateView.as_view(), name='add_budget'),
    path('budget/detail/<uuid:identifier>', views.BudgetDetailView.as_view(), name="detail_budget"),
    path('budget/edit/<uuid:identifier>', views.BudgetUpdateView.as_view(), name="update_budget"),
    path('budget/delete/<uuid:identifier>', views.BudgetDeleteView.as_view(), name = "delete_budget"),
    path('budget/delete_file/<int:file_id>', views.deleting_file_budget, name="delete_file_budget"),

    path('bills/', views.bills, name="list_bills"),
    path('categories_bills/', views.categories_bills, name="categories_bills"),
    path('bills_reports/', views.bills_reports, name="bills_reports"),
    path('bills_add/', views.bills_add, name="bills_add"),


    path('departments/', views.departments, name="departments"),
    path('departments_add/', views.departments_add, name="departments_add"),
    path('roles/', views.roles, name="roles"),
    path('roles_add/', views.roles_add, name="roles_add"),
    path('roles_users/', views.roles_users, name="roles_users"),
    path('roles_users_add/', views.roles_users_add, name="roles_users_add"),
]
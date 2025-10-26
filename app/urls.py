from . import views
from django.urls import path

app_name = 'app'

urlpatterns = [
    path('', views.root_redirect, name='root_redirect'),  # redirect from /
    path('index/', views.index, name='index'),

    path('budget/', views.BudgetListView.as_view(), name='budget'),
    path('details_budget/', views.details_budget, name='details_budget'),
    path('add_budget/', views.BudgetCreateView.as_view(), name='add_budget'),
    
    path('bills/', views.bills, name="bills"),
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
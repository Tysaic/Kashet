from . import views
from django.urls import path

app_name = 'app'

urlpatterns = [
    path('', views.root_redirect, name='root_redirect'),  # redirect from /
    path('index', views.index, name='index'),
    path('budget', views.budget, name='budget'),
    path('budget-details', views.details_budget, name='details_budget'),
    path('budget-add', views.add_budget, name='add_budget'),
    path('bills', views.bills, name="bills"),
    path('bills-categories', views.categories_bills, name="categories_bills"),
    path('bills-reports', views.bills_reports, name="bills_reports"),
    path('bills-add', views.bills_add, name="bills_add"),
    path('departments', views.departments, name="departments"),
    path('departments-add', views.departments_add, name="departments_add"),
    path('roles', views.roles, name="roles"),
    path('roles-add', views.roles_add, name="roles_add"),
    path('roles-users', views.roles_users, name="roles_users"),
    path('roles-users-add', views.roles_users_add, name="roles_users_add"),
]
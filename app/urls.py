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

    path('list_bills/', views.BillListView.as_view(), name="list_bills"),
    path('bills/add_bill/', views.BillCreateView.as_view(), name="add_bill"),
    path('bills/detail/<uuid:identifier>', views.BillDetailView.as_view(), name='detail_bill'),
    path('bills/edit/<uuid:identifier>', views.BillUpdateView.as_view(), name='update_bill'),
    path('bills/delete/<uuid:identifier>', views.BillDeleteView.as_view(), name='delete_bill'),
    path('bills/delete_file/<int:file_id>', views.deleting_file_bill, name='delete_file_bill'),

    path('categories_bills/', views.CategoryBillsList.as_view(), name="categories_bills"),
    path('categories_bills/add/', views.CategoryBillCreateView.as_view(), name="add_categories_bills"),
    path('categories_bills/edit/<int:id>', views.CategoryBillUpdateView.as_view(), name="update_categories_bills"),
    path('categories_bills/delete/<int:id>', views.CategoryBillDeleteView.as_view(), name='delete_categories_bills'),
    
    path('departments/', views.DepartmentListView.as_view(), name="list_departments"),
    path('departments/details/<int:id>', views.DepartmentDetailsView.as_view(), name="details_department"),
    path('departments/add/', views.DepartmentCreateView.as_view(), name="add_departments"),

    path('bills_reports/', views.bills_reports, name="bills_reports"),

    path('roles/', views.roles, name="roles"),
    path('roles_add/', views.roles_add, name="roles_add"),
    path('roles_users/', views.roles_users, name="roles_users"),
    path('roles_users_add/', views.roles_users_add, name="roles_users_add"),
]
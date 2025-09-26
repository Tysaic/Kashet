from . import views
from django.urls import path

app_name = 'app'

urlpatterns = [
    path('', views.root_redirect, name='root_redirect'),  # redirect from /
    path('index', views.index, name='index'),
    path('budget', views.budget, name='budget'),
]
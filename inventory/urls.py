from django.urls import path
from . import views

urlpatterns = [
    path('', views.inventory_log_list, name='inventory_log_list'),
]
# Core Django imports
from django.urls import path

# This project apps imports
from . import views

app_name = 'inventories'

urlpatterns = [

    # This is the landing page
    # /inventories/
    path('', views.ne_list, name='index'),

    # ex: /inventories/circuit/
    path('circuit/', views.circuit_list, name='circuit_list'),

    # ex: /inventories/ne/
    path('ne/', views.ne_list, name='ne_list'),

    # ex: /inventories/ne/5/
    path('ne/<int:pk>/', views.ne_detail, name='ne_detail'),

]

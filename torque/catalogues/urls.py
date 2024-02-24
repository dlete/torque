# Core Django imports
from django.urls import path

# This project apps imports
from . import views

app_name = 'catalogues'

urlpatterns = [
    # ex: /catalogues/transceiver_all/
    path('transceiver_all/', views.transceiver_all, name='transceiver_all'),
]

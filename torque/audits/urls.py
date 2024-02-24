# Core Django imports
from django.urls import path

# This project apps imports
from . import views

app_name = 'audits'

urlpatterns = [
    # test ex: /audits/ne_bogus/5/
    path('ne_bogus/<int:ne_id>/',
        views.ne_bogus, name='ne_bogus'
    ),

    # ex: /audits/ne_all/5/
    path('ne_all/<int:ne_id>/',
        views.ne_all, name='ne_all'
    ),

    # ex: /audits/ne_chassis_alarms/5/
    path('ne_chassis_alarms/<int:ne_id>/',
        views.ne_chassis_alarms, name='ne_alarms'
    ),

    # ex: /audits/ne_duplicate_ip/5/
    path('ne_duplicate_ip/<int:ne_id>/',
        views.ne_duplicate_ip, name='ne_duplicate_ip'
    ),

    # ex: /audits/ne_ibgp/5/
    path('ne_ibgp/<int:ne_id>/',
        views.ne_ibgp, name='ne_ibgp'
    ),

    # ex: /audits/ne_intopticdiag/5/
    path('ne_intopticdiag/<int:ne_id>/',
        views.ne_intopticdiag, name='ne_intopticdiag'
    ),

    # ex: /audits/ne_isis/5/
    path('ne_isis/<int:ne_id>/',
        views.ne_isis, name='ne_isis'
    ),

    # ex: /audits/ne_keywords/5/
    path('ne_keywords/<int:ne_id>/',
        views.ne_keywords, name='ne_keywords'
    ),

    # ex: /audits/ne_lldp/5/
    path('ne_lldp/<int:ne_id>/',
        views.ne_lldp, name='ne_lldp'
    ),

    # ex: /audits/ne_nni_description/5/
    path('ne_nni_description/<int:ne_id>/',
        views.ne_nni_description, name='ne_nni_description'
    ),

    # ex: /audits/ne_os/5/
    path('ne_os/<int:ne_id>/',
        views.ne_os, name='ne_os'
    ),

    # ex: /audits/ne_phyport/5/
    path('ne_phyport/<int:ne_id>/',
        views.ne_phyport, name='ne_phyport'
    ),

    # ex: /audits/ne_transceiver/5/
    path('ne_transceiver/<int:ne_id>/',
        views.ne_transceiver, name='ne_transceiver'
    ),

]

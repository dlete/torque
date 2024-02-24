# Core Django imports
from django.conf.urls import url
from django.conf.urls import include
from django.urls import path

# Third-party app imports
from rest_framework import routers

# This project apps imports
from . import views

app_name = 'apiv1'
router = routers.DefaultRouter()

router.register(
    r'catalogues/ethernetphysicallayer',
    views.EthernetPhysicalLayerViewSet
)
router.register(
    r'catalogues/manufacturer', 
    views.ManufacturerViewSet
)
router.register(
    r'catalogues/partnumber', 
    views.PartNumberViewSet
)
router.register(
    r'catalogues/supplier', 
    views.SupplierViewSet
)
router.register(
    r'catalogues/transceiverformfactor', 
    views.TransceiverFormFactorViewSet
)
router.register(
    r'catalogues/transceiver',
    views.TransceiverViewSet
)
router.register(
    r'catalogues/os',
    views.OsViewSet
)


router.register(
    r'inventories/circuit',
    views.CircuitViewSet
)
router.register(
    r'inventories/ne',
    views.NeViewSet
)
router.register(
    r'inventories/oscredential',
    views.OsCredentialViewSet
)


urlpatterns = [

    #url(r'^', include(router.urls)),
    path('', include(router.urls)),
    # api-auth MUST be in the top level url.py. I leave this line here so that
    # it servers as reminder.
    #url(r'^api-auth/', 
    #    include('rest_framework.urls', namespace='rest_framework')
    #),
    # Use for troubleshooting. Leave here just in case. 
    #url(r'^custom/ne/(?P<ne_id>[0-9]+)/bogus/$', views.CustomGet.as_view()),

    #url(r'^audits/ne_all/(?P<ne_id>[0-9]+)/$',
    path('audits/ne_all/<int:ne_id>/',
        views.audit_ne_all.as_view()
    ),

    #url(r'^audits/ne_bogus/(?P<ne_id>[0-9]+)/$',
    path('audits/ne_bogus/<int:ne_id>/',
        views.audit_ne_bogus.as_view()
    ),
    #url(r'^audits/ne_chassis_alarms/(?P<ne_id>[0-9]+)/$', 
    path('audits/ne_chassis_alarms/<int:ne_id>/',
        views.audit_ne_chassis_alarms.as_view()
    ),
    #url(r'^audits/ne_duplicate_ip/(?P<ne_id>[0-9]+)/$',
    path('audits/ne_duplicate_ip/<int:ne_id>/',
        views.audit_ne_duplicate_ip.as_view()
    ),
    #url(r'^audits/ne_ibgp/(?P<ne_id>[0-9]+)/$',
    path('audits/ne_ibgp/<int:ne_id>/',
        views.audit_ne_ibgp.as_view()
    ),
    #url(r'^audits/ne_intopticdiag/(?P<ne_id>[0-9]+)/$',
    path('audits/ne_intopticdiag/<int:ne_id>/',
        views.audit_ne_intopticdiag.as_view()
    ),
    #url(r'^audits/ne_isis/(?P<ne_id>[0-9]+)/$',
    path('audits/ne_isis/<int:ne_id>/',
        views.audit_ne_isis.as_view()
    ),
    #url(r'^audits/ne_keywords/(?P<ne_id>[0-9]+)/$',
    path('audits/ne_keywords/<int:ne_id>/',
        views.audit_ne_keywords.as_view()
    ),
    #url(r'^audits/ne_lldp/(?P<ne_id>[0-9]+)/$',
    path('audits/ne_lldp/<int:ne_id>/',
        views.audit_ne_lldp.as_view()
    ),
    #url(r'^audits/ne_nni_description/(?P<ne_id>[0-9]+)/$',
    path('audits/ne_nni_description/<int:ne_id>/',
        views.audit_ne_nni_description.as_view()
    ),
    #url(r'^audits/ne_os/(?P<ne_id>[0-9]+)/$',
    path('audits/ne_os/<int:ne_id>/',
        views.audit_ne_os.as_view()
    ),
    #url(r'^audits/ne_phyport/(?P<ne_id>[0-9]+)/$',
    path('audits/ne_phyport/<int:ne_id>/',
        views.audit_ne_phyport.as_view()
    ),
    #url(r'^audits/ne_transceiver/(?P<ne_id>[0-9]+)/$',
    path('audits/ne_transceiver/<int:ne_id>/',
        views.audit_ne_transceiver.as_view()
    ),

]

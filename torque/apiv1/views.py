'''
To do:
    check http://www.django-rest-framework.org/tutorial/2-requests-and-responses/
    for this
    REST framework provides two wrappers you can use to write API views.
            
    The @api_view decorator for working with function based views.
    The APIView class for working with class-based views.
Note:
    VERY IMPORTANT, need to import django.db models to be able to import
    models from other apps.
'''
            
# Core Django imports
from django.db import models
from django.shortcuts import render

# Third-party app imports
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

# This project apps imports
from catalogues.models import Manufacturer
from catalogues.models import EthernetPhysicalLayer
from catalogues.models import PartNumber
from catalogues.models import Supplier
from catalogues.models import TransceiverFormFactor
from catalogues.models import Transceiver
from catalogues.models import Os

# REMOVE ONCE WE ARE SURE inventory APP IS NOT NEEDED
#from inventory.models import Circuit
#from inventory.models import Ne
#from inventory.models import OsCredential

from inventories.models import Circuit
from inventories.models import Ne
from inventories.models import OsCredential

from .serializers import EthernetPhysicalLayerSerializer
from .serializers import ManufacturerSerializer
from .serializers import PartNumberSerializer
from .serializers import SupplierSerializer
from .serializers import TransceiverFormFactorSerializer
from .serializers import TransceiverSerializer
from .serializers import OsSerializer
from .serializers import CircuitSerializer
from .serializers import NeSerializer
from .serializers import OsCredentialSerializer


class CustomGet(APIView):
    '''
    A custom endpoint for GET request.
    Use it for troubleshooting. Leave here just in case.
    Reference is:
    https://eureka.ykyuen.info/2014/08/28/django-rest-framework-create
    -endpoints-for-custom-actions/
    '''
    def get(self, request, format=None):
        '''
        Return a hardcoded response.
        '''
        return Response({"success": True, "content": "Hello World!"})


class audit_ne_all(APIView):
    def get(self, request, ne_id, format=None):
        from audits.libs import audits_ne
        report_dictionary = audits_ne.ne_audit_all(ne_id)
        return Response(report_dictionary)


class audit_ne_bogus(APIView):
    def get(self, request, ne_id, format=None):
        from audits.libs import audits_ne
        report_dictionary = audits_ne.ne_audit_bogus(ne_id)
        return Response(report_dictionary)


class audit_ne_chassis_alarms(APIView):
    def get(self, request, ne_id, format=None):
        from audits.libs import audits_ne
        report_dictionary = audits_ne.ne_audit_chassis_alarms(ne_id)
        return Response(report_dictionary)


class audit_ne_duplicate_ip(APIView):
    def get(self, request, ne_id, format=None):
        from audits.libs import audits_ne
        report_dictionary = audits_ne.ne_audit_duplicate_ip(ne_id)
        return Response(report_dictionary)


class audit_ne_ibgp(APIView):
    def get(self, request, ne_id, format=None):
        from audits.libs import audits_ne
        report_dictionary = audits_ne.ne_audit_ibgp(ne_id)
        return Response(report_dictionary)


class audit_ne_intopticdiag(APIView):
    def get(self, request, ne_id, format=None):
        from audits.libs import audits_ne
        report_dictionary = audits_ne.ne_audit_intopticdiag(ne_id)
        return Response(report_dictionary)


class audit_ne_isis(APIView):
    def get(self, request, ne_id, format=None):
        from audits.libs import audits_ne
        report_dictionary = audits_ne.ne_audit_isis(ne_id)
        return Response(report_dictionary)


class audit_ne_keywords(APIView):
    def get(self, request, ne_id, format=None):
        from audits.libs import audits_ne
        report_dictionary = audits_ne.ne_audit_keywords(ne_id)
        return Response(report_dictionary)


class audit_ne_lldp(APIView):
    def get(self, request, ne_id, format=None):
        from audits.libs import audits_ne
        report_dictionary = audits_ne.ne_audit_lldp(ne_id)
        return Response(report_dictionary)


class audit_ne_nni_description(APIView):
    def get(self, request, ne_id, format=None):
        from audits.libs import audits_ne
        report_dictionary = audits_ne.ne_audit_nni_description(ne_id)
        return Response(report_dictionary)


class audit_ne_os(APIView):
    def get(self, request, ne_id, format=None):
        from audits.libs import audits_ne
        report_dictionary = audits_ne.ne_audit_os(ne_id)
        return Response(report_dictionary)


class audit_ne_phyport(APIView):
    def get(self, request, ne_id, format=None):
        from audits.libs import audits_ne
        report_dictionary = audits_ne.ne_audit_phyport(ne_id)
        return Response(report_dictionary)


class audit_ne_transceiver(APIView):
    def get(self, request, ne_id, format=None):
        from audits.libs import audits_ne
        report_dictionary = audits_ne.ne_audit_transceiver(ne_id)
        return Response(report_dictionary)


class EthernetPhysicalLayerViewSet(viewsets.ModelViewSet):
    '''
    list:
    Return al list of all the existing EthernetPhysicalLayer.

    create:
    Create a new EthernetPhysicalLayer.

    retrieve:
    Return the given EthernetPhysicalLayer.

    update:
    Update the given EthernetPhysicalLayer.

    partial_update:
    Update part of the given EthernetPhysicalLayer.

    destroy:
    Delete the given EthernetPhysicalLayer.
    '''
    queryset = EthernetPhysicalLayer.objects.all()
    serializer_class = EthernetPhysicalLayerSerializer

class ManufacturerViewSet(viewsets.ModelViewSet):
    '''
    list:
    Return al list of all the existing Manufacturer.

    create:
    Create a new Manufacturer.

    retrieve:
    Return the given Manufacturer.

    update:
    Update the given Manufacturer.

    partial_update:
    Update part of the given Manufacturer.

    destroy:
    Delete the given Manufacturer.
    '''
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer

class PartNumberViewSet(viewsets.ModelViewSet):
    '''
    list:
    Return al list of all the existing PartNumber.

    create:
    Create a new PartNumber.

    retrieve:
    Return the given PartNumber.

    update:
    Update the given PartNumber.

    partial_update:
    Update part of the given PartNumber.

    destroy:
    Delete the given PartNumber.
	'''
    queryset = PartNumber.objects.all()
    serializer_class = PartNumberSerializer

class SupplierViewSet(viewsets.ModelViewSet):
    '''
    list:
    Return al list of all the existing Supplier.

    create:
    Create a new Supplier.

    retrieve:
    Return the given Supplier.

    update:
    Update the given Supplier.

    partial_update:
    Update part of the given Supplier.

    destroy:
    Delete the given Supplier.
    '''
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

class TransceiverFormFactorViewSet(viewsets.ModelViewSet):
    '''
    list:
    Return al list of all the existing TransceiverFormFactor.

    create:
    Create a new TransceiverFormFactor.

    retrieve:
    Return the given TransceiverFormFactor.

    update:
    Update the given TransceiverFormFactor.

    partial_update:
    Update part of the given TransceiverFormFactor.

    destroy:
    Delete the given TransceiverFormFactor.
    '''
    queryset = TransceiverFormFactor.objects.all()
    serializer_class = TransceiverFormFactorSerializer

class TransceiverViewSet(viewsets.ModelViewSet):
    '''
    list:
    Return al list of all the existing Transceiver.

    create:
    Create a new Transceiver.

    retrieve:
    Return the given Transceiver.

    update:
    Update the given Transceiver.

    partial_update:
    Update part of the given Transceiver.

    destroy:
    Delete the given Transceiver.
    '''
    queryset = Transceiver.objects.all()
    serializer_class = TransceiverSerializer


class OsViewSet(viewsets.ModelViewSet):
    '''
    list:
    Return al list of all the existing Operating Systems.

    create:
    Create a new Operating System.

    retrieve:
    Return the given Operating System.

    update:
    Update the given Operating System.

    partial_update:
    Update part of the given Operating System.

    destroy:
    Delete the given Operating System.
    '''
    queryset = Os.objects.all()
    serializer_class = OsSerializer


class CircuitViewSet(viewsets.ModelViewSet):
    '''
    list:
    Return al list of all the existing Circuit.

    create:
    Create a new Circuit.

    retrieve:
    Return the given Circuit.

    update:
    Update the given Circuit.

    partial_update:
    Update part of the given Circuit.

    destroy:
    Delete the given Circuit.
    '''
    queryset = Circuit.objects.all()
    serializer_class = CircuitSerializer

class NeViewSet(viewsets.ModelViewSet):
    '''
    list:
    Return al list of all the existing Ne.

    create:
    Create a new Ne.

    retrieve:
    Return the given Ne.

    update:
    Update the given Ne.

    partial_update:
    Update part of the given Ne.

    destroy:
    Delete the given Ne.
    '''
    queryset = Ne.objects.all()
    serializer_class = NeSerializer

class OsCredentialViewSet(viewsets.ModelViewSet):
    '''
    list:
    Return al list of all the existing OsCredential.

    create:
    Create a new OsCredential.

    retrieve:
    Return the given OsCredential.

    update:
    Update the given OsCredential.

    partial_update:
    Update part of the given OsCredential.

    destroy:
    Delete the given OsCredential.
    '''
    queryset = OsCredential.objects.all()
    serializer_class = OsCredentialSerializer

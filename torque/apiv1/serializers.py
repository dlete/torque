# Core Django imports
# Need to import models from django.db to be able to import models 
# from other apps.
from django.db import models

# Third-party app imports
from rest_framework import serializers

# This project apps imports
from catalogues.models import Manufacturer
from catalogues.models import EthernetPhysicalLayer
from catalogues.models import PartNumber
from catalogues.models import Supplier
from catalogues.models import TransceiverFormFactor
from catalogues.models import Transceiver
from catalogues.models import Os

#from inventory.models import Circuit
#from inventory.models import Ne
#from inventory.models import OsCredential

from inventories.models import Circuit
from inventories.models import Ne
from inventories.models import OsCredential


# HyperlinkedModelSerializer vs. ModelSerializer??? see notes


class EthernetPhysicalLayerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EthernetPhysicalLayer
        #fields = '__all__'  
        # in Python ('my_field') is a string. To make a single-element tuple 
        # you need a comma: ('my_field',).
        # https://stackoverflow.com/questions/35676293/django-rest-framework
        #-tuple-being-interpreted-as-a-string
        fields = ('id', 'name',)


class ManufacturerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ('id', 'name', 'abbreviation')


class PartNumberSerializer(serializers.ModelSerializer):
#class PartNumberSerializer(serializers.HyperlinkedModelSerializer):
    # Represent the target of the relationship using its __unicode__ method.
    # if we do not put StringRelatedField then it will display the key, the digit.
    # http://www.django-rest-framework.org/api-guide/relations/
    #manufacturer = serializers.StringRelatedField(many=False)
    class Meta:
        model = PartNumber
        fields = ('id', 'part_number', 'description', 'manufacturer')


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ('id', 'name', 'abbreviation')


class TransceiverFormFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransceiverFormFactor
        fields = ('id', 'name', 'description')


class TransceiverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transceiver
        fields = ('id', 'part_number', 'form_factor', 'type_code', 
            'powerbudget', 'receive_min', 'receive_max'
        )

class OsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Os
        fields = ('id', 'manufacturer', 'family', 'version')


class CircuitSerializer(serializers.ModelSerializer):
    #supplier = serializers.StringRelatedField(many=False)
    supplier = serializers.PrimaryKeyRelatedField(
        many=False, 
        queryset=Supplier.objects.all()
    )
    class Meta:
        model = Circuit
        fields = ('id', 'supplier', 'circuit_id', 'a_end_description',
            'b_end_description', 'circuit_type', 'circuit_info'
        )


class NeSerializer(serializers.ModelSerializer):
    #os_credential = serializers.StringRelatedField(many=False)

    class Meta:
        model = Ne
        fields = ('id', 'fqdn', 'os_credential')


class OsCredentialSerializer(serializers.ModelSerializer):
    class Meta:
        model = OsCredential
        fields = ('id', 'username')

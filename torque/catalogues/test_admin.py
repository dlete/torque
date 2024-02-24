'''
Notes/reference:
    On "self.app_admin = TransceiverAdmin(Transceiver, AdminSite())" below:
    THIS IS THE KEY!!!!!
    https://groups.google.com/forum/#!msg/django-users/2zN3BlFLIFE/EW1STOoo1uEJ
    maybe also check for examples?
    https://github.com/django/django/blob/master/tests/modeladmin/tests.py
'''

# Core Django imports
from django.test import TestCase
from django.contrib.admin.sites import AdminSite

# This project apps imports
from .admin import TransceiverAdmin
from .models import Manufacturer
from .models import PartNumber
from .models import TransceiverFormFactor
from .models import Transceiver


class CataloguesAdminTest(TestCase):

    def setUp(self):
        '''
        Establish fixtures for each individual test case.
        '''
        Manufacturer.objects.create(
            name = "Acme, Inc.",
            abbreviation = "ACME",
        )
        m = Manufacturer.objects.get(abbreviation='ACME')

        PartNumber.objects.create(
            part_number = "PN.1234",
            description = "Part Number for testing",
            manufacturer = m,
        )
        pn = PartNumber.objects.get(part_number='PN.1234')

        TransceiverFormFactor.objects.create(
            name = "SFP",
            description = "Small Form-factor Pluggable",
        )
        tff = TransceiverFormFactor.objects.get(name='SFP')

        Transceiver.objects.create(
            part_number = pn,
            form_factor = tff,
            type_code = "10GBASELR",
            powerbudget = 27.00,
            receive_min = -13.00,
            receive_max = -1,
        )
        t = Transceiver.objects.get(type_code='10GBASELR')
        
        # SEE NOTE ABOVE!!
        self.app_admin = TransceiverAdmin(Transceiver, AdminSite())


    def test_part_number_description_returns_description(self):
        t = Transceiver.objects.get(type_code='10GBASELR')
        #self.app_admin.part_number_description(request, t)
        #print(self.app_admin.part_number_description(t))
        #print(t.part_number.description)
        self.assertEqual(
            self.app_admin.part_number_description(t),
            t.part_number.description
        )

    def test_part_number_manufacturer_returns_manufacturer(self):
        t = Transceiver.objects.get(type_code='10GBASELR')
        #print(self.app_admin.part_number_manufacturer(t))
        #print(t.part_number.manufacturer)
        self.assertEqual(
            self.app_admin.part_number_manufacturer(t),
            t.part_number.manufacturer
        )


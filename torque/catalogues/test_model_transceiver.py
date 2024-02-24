# Core Django imports
from django.test import TestCase

# This project apps imports
from .models import Manufacturer
from .models import PartNumber
from .models import Transceiver
from .models import TransceiverFormFactor


class TransceiverModelTests(TestCase):

    def setUp(self):
        '''
        Establish fixtures for each individual test case.
        '''
        Manufacturer.objects.create(
            name = "Acme, Inc.",
            abbreviation = "ACME",
        )
        m = Manufacturer.objects.get(abbreviation = "ACME")

        PartNumber.objects.create(
            part_number = "PN.1234",
            description = "Part Number for testing",
            manufacturer = m,
        )
        pn = PartNumber.objects.get(part_number = "PN.1234")

        TransceiverFormFactor.objects.create(
            name = "SFP",
            description = "Small Form-factor Pluggable",
        )
        tff = TransceiverFormFactor.objects.get(name = "SFP")

        Transceiver.objects.create(
            part_number = pn,
            form_factor = tff,
            type_code = "10GBASELR",
            powerbudget = 27.00,
            receive_min = -13.00,
            receive_max = -1,
        )
        t = Transceiver.objects.get(type_code = "10GBASELR")


    def test_cataloques_transceiver__str__(self):
        '''
        Test Transceiver Method __str__

        Retrieve object from the database.
        Verify that ouput of __str__() method is the same than object username.
        '''
        t = Transceiver.objects.get(type_code = "10GBASELR")
        self.assertEqual(t.__str__(), t.part_number.part_number)


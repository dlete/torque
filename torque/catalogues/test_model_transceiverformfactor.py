# Core Django imports
from django.test import TestCase

# This project apps imports
from .models import Manufacturer
from .models import PartNumber
from .models import TransceiverFormFactor


class TransceiverFormFactorModelTests(TestCase):

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


    def test_cataloques_transceiverformfactor__str__(self):
        '''
        Test TransceiverFormFactor Method __str__

        Retrieve object from the database.
        Verify that ouput of __str__() method is the same than object username.
        '''
        tff = TransceiverFormFactor.objects.get(name = "SFP")
        self.assertEqual(tff.__str__(), tff.name)


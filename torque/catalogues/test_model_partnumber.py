# Core Django imports
from django.test import TestCase

# This project apps imports
from .models import Manufacturer
from .models import PartNumber


class PartNumberModelTests(TestCase):

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


    def test_cataloques_partnumber__str__(self):
        '''
        Test Manufacturer Method __str__

        Retrieve object from the database.
        Verify that ouput of __str__() method is the same than object username.
        '''
        pn = PartNumber.objects.get(part_number = "PN.1234")
        self.assertEqual(pn.__str__(), pn.part_number)


# Core Django imports
from django.test import TestCase

# This project apps imports
from .models import Manufacturer


class ManufacturerModelTests(TestCase):

    def setUp(self):
        '''
        Establish fixtures for each individual test case.
        '''
        Manufacturer.objects.create(
            name = "Acme, Inc.",
            abbreviation = "ACME",
        )
        m = Manufacturer.objects.get(abbreviation = "ACME")


    def test_cataloques_manufacturer__str__(self):
        '''
        Test Manufacturer Method __str__

        Retrieve object from the database.
        Verify that ouput of __str__() method is the same than object username.
        '''
        manufacturer = Manufacturer.objects.get(abbreviation = "ACME")
        self.assertEqual(manufacturer.__str__(), manufacturer.name)


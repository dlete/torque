# Core Django imports
from django.test import TestCase

# This project apps imports
from .models import Manufacturer
from .models import Os


class OsModelTests(TestCase):

    def setUp(self):
        '''
        Establish fixtures for each individual test case.
        '''
        Manufacturer.objects.create(
            name = "Acme, Inc.",
            abbreviation = "ACME",
        )
        m = Manufacturer.objects.get(abbreviation = "ACME")

        Os.objects.create(
            manufacturer = m,
            family = "XR",
            version = "4.4.7",
        )
        o = Os.objects.get(manufacturer = m, family = "XR", version = "4.4.7")


    def test_cataloques_os__str__(self):
        '''
        Test Os Method __str__

        Retrieve object from the database.
        Verify that ouput of __str__() method is the same than object username.
        '''
        m = Manufacturer.objects.get(abbreviation = "ACME")
        o = Os.objects.get(manufacturer = m, family = "XR", version = "4.4.7")
        self.assertEqual(o.__str__(), o.manufacturer.name)


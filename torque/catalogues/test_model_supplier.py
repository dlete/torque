# Core Django imports
from django.test import TestCase
from django.db import IntegrityError

# This project apps imports
from .models import Supplier


class SupplierModelTests(TestCase):

    def setUp(self):
        '''
        Establish fixtures for each individual test case.
        '''
        Supplier.objects.create(
            name = "Acme, Inc.",
            abbreviation = "ACME",
        )
        s = Supplier.objects.get(abbreviation = "ACME")

    def test_catalogues_supplier__str__(self):
        '''
        Test Supplier Method __str__()
        
        Retrieve object from the database.
        Verify that ouput of __str__() method is the same than object username.
        '''
        supplier = Supplier.objects.get(name='Acme, Inc.')
        self.assertEqual(supplier.__str__(), supplier.name)


    def test_catalogues_supplier_unique_name(self):
        '''
        Test Supplier name field is unique.

        Creating a Supplier object with the same name than an existing Supplier
        (that is the Supplier created in setUp) raises an 
        IntegrityError exception.
        '''
        s = Supplier.objects.get(abbreviation = "ACME")
        with self.assertRaises(IntegrityError):
            Supplier.objects.create(
                name = "Acme, Inc.",
                abbreviation = "different_abbreviation",
            )

    def test_catalogues_supplier_name_max_lenght(self):
        '''
        Test Supplier name max_lenght.

        Retrieve object from the database.
        Verify that max_lenght object fields attribute is as defined in model.
        '''
        s = Supplier.objects.get(abbreviation = "ACME")
        max_length_name = s._meta.get_field('name').max_length
        self.assertEqual(max_length_name, 255)


    def test_catalogues_supplier_unique_abbreviation(self):
        '''
        Test Supplier abbreviation field is unique.

        Creating a Supplier object with the same abbreviation than an existing 
		Supplier (that is the Supplier created in setUp) raises an
        IntegrityError exception.
        '''
        s = Supplier.objects.get(abbreviation = "ACME")
        with self.assertRaises(IntegrityError):
            Supplier.objects.create(
                name = "different name",
                abbreviation = "ACME",
            )


    def test_catalogues_supplier_abbreviation_max_lenght(self):
        '''
        Test Supplier abbreviation max_lenght.

        Retrieve object from the database.
        Verify that max_lenght object fields attribute is as defined in model.
        '''
        s = Supplier.objects.get(abbreviation = "ACME")
        max_length_abbreviation = s._meta.get_field('abbreviation').max_length
        self.assertEqual(max_length_abbreviation, 50)


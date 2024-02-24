# Core Django imports
from django.test import TestCase
from django.db import IntegrityError
from django.db import models

# This project apps imports
from .models import Circuit
from catalogues.models import Supplier


'''
In this file: Unittest for model Circuit

TO DO
'''


class NeModelTests(TestCase):

    def setUp(self):
        '''
        Establish fixtures for each individual test case.
        '''
        Supplier.objects.create(
            name = "test supplier name 1",
            abbreviation = "tsa1",
        )
        supplier1 = Supplier.objects.get(abbreviation = "tsa1")

        Circuit.objects.create(
            supplier = supplier1,
            circuit_id = "cid1",
            a_end_description = "c1_a_end_desc",
            b_end_description = "c1_b_end_desc",
            circuit_type = "Dark fibre",
            circuit_info = "Bogus circuit #1 for unittest",
        )
        circuit1 = Circuit.objects.get(circuit_id = "cid1")

    def test_circuit_method__str__(self):
        '''
        Test Circuit Method __str__

        Retrieve object from the database.
        Verify that __str__() method output is the same than object circuit_id.
        '''
        c = Circuit.objects.get(circuit_id = "cid1")
        self.assertEqual(c.__str__(), c.circuit_id)


# Core Django impor
from django.test import TestCase

# This project apps imports
from .models import EthernetPhysicalLayer


class EthernetPhysicalLayerModelTests(TestCase):

    def setUp(self):
        '''
        Establish fixtures for each individual test case.
        '''
        EthernetPhysicalLayer.objects.create(
            name = "LR",
        )
        epl = EthernetPhysicalLayer.objects.get(name='LR')


    def test_ethernetphysicallayer__str__(self):
        '''
        Test EthernetPhysicalLayer Method __str__

        Retrieve object from the database.
        Verify that ouput of __str__() method is the same than object username.
        '''

        epl = EthernetPhysicalLayer.objects.get(name='LR')
        self.assertEqual(epl.__str__(), epl.name)


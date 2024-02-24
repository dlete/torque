# Core Django imports
from django.test import TestCase
from django.urls import reverse

# This project apps imports
from .models import EthernetPhysicalLayer
from .models import Manufacturer
from .models import PartNumber
from .models import Transceiver
from .models import TransceiverFormFactor


class CataloguesViewsTests(TestCase):

    def setUp(self):
        '''
        Establish fixtures for each individual test case.
        '''
        Manufacturer.objects.create(
            name = "Manufacturer1",
            abbreviation = "Manu1",
        )
        m = Manufacturer.objects.get(abbreviation='Manu1')

        PartNumber.objects.create(
            part_number = "pn1234",
            description = "Part to do many things",
            manufacturer = m,
        )
        pn = PartNumber.objects.get(part_number='pn1234')

        TransceiverFormFactor.objects.create(
            name = "SPF",
            description = "Small Form-factor Pluggable",
        )
        tff = TransceiverFormFactor.objects.get(name='SPF')

        Transceiver.objects.create(
            part_number = pn,
            form_factor = tff,
            type_code = "10GBASELR",
            powerbudget = 27.00,
            receive_min = -13.00,
            receive_max = -1,
        )
        t = Transceiver.objects.get(type_code='10GBASELR')


    def test_catalogues_transceiver_all(self):
        '''
        Test Catalogues view transceiver_all.
        '''
        response = self.client.get(reverse('catalogues:transceiver_all'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Transceivers catalogue")
        self.assertQuerysetEqual(
            response.context['transceiver_all'],
            [repr(t) for t in Transceiver.objects.all()]
        )

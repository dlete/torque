'''
This file does test the Transceiver class:
 - List all objects.
 - Create, Read, Update (with the Put verb) and Delete a valid and an
   invalid object.
 - Update (with the Patch verb) a valid and an invalid object.


To-do:


Note:
The 'reverse' facility is used very much in these tests. The 'name' of the 
URL pattern in apiv1/urls.py is automatically generated based on the queryset
attribute of the viewset, if it has one (our viewset all do have a queryset).
See: http://www.django-rest-framework.org/api-guide/routers/ for reference.

Does use the standard Django Client.
Does NOT use the DRF APIClient or RequestClient
'''

# Python standard libraries imports
# needed for the Patch verbs
import json

# Core Django imports
from django.contrib.auth.models import User
from django.db import models
from django.test import Client
from django.test import TestCase
from django.urls import reverse

# Third-party app imports
from rest_framework import status

# This project apps imports
from catalogues.models import Manufacturer
from catalogues.models import PartNumber
from catalogues.models import Transceiver
from catalogues.models import TransceiverFormFactor
from .serializers import ManufacturerSerializer
from .serializers import PartNumberSerializer
from .serializers import TransceiverSerializer
from .serializers import TransceiverFormFactorSerializer


# Instantiate Client. Will use this instance throught all the tests.
client = Client()


class APITransceiverTest(TestCase):

    def setUp(self):
        '''
        Establish fixtures for each individual test case.
        '''
        Manufacturer.objects.create(
            name = "Manufacturer 1",
            abbreviation = "manu1",
        )
        m1 = Manufacturer.objects.get(abbreviation = "manu1")


        PartNumber.objects.create(
            part_number = 'partnumber1',
            description = 'partnumber1 description',
            manufacturer = m1
        )
        pn1 = PartNumber.objects.get(part_number='partnumber1')


        TransceiverFormFactor.objects.create(
            name = "TransceiverFF1",
            description = "TransceiverFF1 description"
        )
        tff1 = TransceiverFormFactor.objects.get(name = "TransceiverFF1")


        Transceiver.objects.create(
            part_number = pn1,
            form_factor = tff1,
            type_code = 'type code 1',
            powerbudget = 13.5,
            receive_min = -23.5,
            receive_max = 1.00
        )
        t1 = Transceiver.objects.get(part_number = pn1.id)


        user = User.objects.create_superuser(
            username='admin',
            password='1234',
            email='demo@demo.com'
        )
        user.save()

        # Make all requests in the context of a logged in session.
        client.login(username='admin', password='1234')


    def tearDown(self):
        '''
        Clear fixtures for each individual test case.
        '''
        # Log out
        client.logout()


    def test_list_all_transceivers(self):
        '''
        List all objects.
        '''
        transceivers = Transceiver.objects.all()
        serializer = TransceiverSerializer(transceivers, many=True)

        response = client.get(reverse('apiv1:transceiver-list'))

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_read_transceiver_valid(self):
        '''
        READ valid.
        '''
        pn1 = PartNumber.objects.get(part_number='partnumber1')
        t1 = Transceiver.objects.get(part_number = pn1.id)

        serializer = TransceiverSerializer(t1)
        response = client.get(
            # Note we can use either pn1.id or t1.id in the args. 
            # That is because there is a OneToOne relationship between
            # the PartNumber and Transceiver objects.
            #reverse('apiv1:transceiver-detail', args=(pn1.id,))
            reverse('apiv1:transceiver-detail', args=(t1.id,))
        )

        '''
        Verify that what we get through a HTTP request is the same than what
        the serializer provides.
        '''
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_read_transceiver_invalid(self):
        '''
        READ invalid.
        '''
        t_id = str(777)

        response = client.get(
            reverse('apiv1:transceiver-detail', args=(t_id,))
        )
        #print(response.data)           # {'detail': 'Not found.'}
        #print(response.status_code)    # 404

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_transceiver_valid(self):
        '''
        CREATE valid.
        '''
        m1 = Manufacturer.objects.get(abbreviation = "manu1")
        tff1 = TransceiverFormFactor.objects.get(name = "TransceiverFF1")

        PartNumber.objects.create(
            part_number = 'partnumber2',
            description = 'partnumber2 description',
            manufacturer = m1
        )
        pn2 = PartNumber.objects.get(part_number='partnumber2')

        data = {
            'part_number': pn2.id,
            'form_factor': tff1.id,
            'type_code': 'LR',
        }
        response = client.post(
            reverse('apiv1:transceiver-list'),
            data,
            format='json'
        )
        t1 = Transceiver.objects.get(part_number = data['part_number'])
        serializer = TransceiverSerializer(t1)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)


    def test_create_transceiver_invalid(self):
        '''
        CREATE invalid.
        '''
        data = {
            'part_number': '',
            'type_code': 'Type Code X'
        }

        response = client.post(
            reverse('apiv1:transceiver-list'),
            data,
            format='json'
        )
        #print("Below is the response.data")
        #print(response.data)    # {'part_number': ["'' value must be an integer."]}

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_patch_transceiver_valid(self):
        '''
        UPDATE (PATCH) valid.
        '''
        pn1 = PartNumber.objects.get(part_number='partnumber1')
        t1 = t1 = Transceiver.objects.get(part_number = pn1.id)
        data = {
            'type_code': 'type code Y',
        }

        response = client.patch(
            reverse('apiv1:transceiver-detail', args=(t1.id,)),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        t = Transceiver.objects.get(pk = t1.id)
        response = client.get(
            reverse('apiv1:transceiver-detail', args=(t.id,)),
        )
        serializer = TransceiverSerializer(t)
        self.assertEqual(response.data, serializer.data)


    def test_patch_transceiver_invalid(self):
        '''
        UPDATE (PATCH) invalid.
        '''
        pn1 = PartNumber.objects.get(part_number='partnumber1')
        t1 = Transceiver.objects.get(part_number = pn1.id)
        data = {
            'part_number': '',
            'type_code': 'Type Code X'
        }

        response = client.patch(
            reverse('apiv1:transceiver-detail', args=(t1.id,)),
            data=json.dumps(data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_update_transceiver_valid(self):
        '''
        UPDATE (PUT) valid.
        '''
        pn1 = PartNumber.objects.get(part_number='partnumber1')
        t1 = Transceiver.objects.get(part_number = pn1.id)
        data = {
            'part_number': pn1.id,
            'type_code': 'type code Y',
        }
        response = client.put(
            reverse('apiv1:transceiver-detail', args=(t1.id,)),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        t = Transceiver.objects.get(part_number = pn1.id)
        response = client.get(
            reverse('apiv1:transceiver-detail', args=(t1.id,)),
        )
        serializer = TransceiverSerializer(t)
        self.assertEqual(response.data, serializer.data)


    def test_update_transceiver_invalid(self):
        '''
        UPDATE (PUT) invalid.
        '''
        pn1 = PartNumber.objects.get(part_number='partnumber1')
        t1 = Transceiver.objects.get(part_number = pn1.id)
        data = {
            'part_number': '',
            'type_code': 'Type Code X'
        }

        response = client.put(
            reverse('apiv1:transceiver-detail', args=(t1.id,)),
            data=json.dumps(data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_delete_transceiver_valid(self):
        '''
        Delete valid.
        '''
        pn1 = PartNumber.objects.get(part_number='partnumber1')
        t1 = Transceiver.objects.get(part_number = pn1.id)

        response = client.delete(
            reverse('apiv1:transceiver-detail',
            args=(t1.id,))
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_delete_transceiver_invalid(self):
        '''
        Delete invalid.
        '''
        pn_id = str(777)

        response = client.delete(
            reverse('apiv1:transceiver-detail',
            args=(pn_id,))
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


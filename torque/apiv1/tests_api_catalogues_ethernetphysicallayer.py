'''
This file does test:
 - List all EthernetPhysicalLayer objects.
 - Create, Read, Update (with the Put verb) and Delete a valid and an 
   invalid EthernetPhysicalLayer object. 
 - Update (with the Patch verb) a valid and an invalid EthernetPhysicalLayer
   object.

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
from catalogues.models import EthernetPhysicalLayer
from .serializers import EthernetPhysicalLayerSerializer


# Instantiate Client. Will use this instance throught all the tests.
client = Client()


class APIEthernetPhysicalLayerTest(TestCase):

    def setUp(self):
        '''
        Establish fixtures for each individual test case.
        '''
        EthernetPhysicalLayer.objects.create(
            name = "EthernetPhysicalLayer 1",
        )
        epl1 = EthernetPhysicalLayer.objects.get(
            name = "EthernetPhysicalLayer 1"
        )

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


    def test_list_all_ethernetphysicallayers(self):
        '''
        List all objects.
        '''
        epls = EthernetPhysicalLayer.objects.all()
        serializer = EthernetPhysicalLayerSerializer(epls, many=True)

        response = client.get(reverse('apiv1:ethernetphysicallayer-list'))

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_read_ethernetphysicallayer_valid(self):
        '''
        READ valid.
        '''
        epl = EthernetPhysicalLayer.objects.get(
            name = "EthernetPhysicalLayer 1"
        )
        serializer = EthernetPhysicalLayerSerializer(epl)

        response = client.get(
            reverse('apiv1:ethernetphysicallayer-detail',
            args=(epl.id,))
        )

        '''
        Verify that what we get through a HTTP request is the same than what
        the serializer provides.
        '''
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_read_ethernetphysicallayer_invalid(self):
        '''
        READ invalid.
        '''
        epl_id = str(777)

        response = client.get(
            reverse('apiv1:ethernetphysicallayer-detail',
            args=(epl_id,))
        )
        #print(response.data)           # {'detail': 'Not found.'}
        #print(response.status_code)    # 404

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_create_ethernetphysicallayer_valid(self):
        '''
        CREATE valid.
        '''
        data = {'name': 'EthernetPhysicalLayer X'}

        response = client.post(
            reverse('apiv1:ethernetphysicallayer-list'),
            data,
            format='json'
        )

        epl = EthernetPhysicalLayer.objects.get(name = data['name'])
        serializer = EthernetPhysicalLayerSerializer(epl)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)


    def test_create_ethernetphysicallayer_invalid(self):
        '''
        CREATE invalid.
        '''
        data = {'name': ''}

        response = client.post(
            reverse('apiv1:ethernetphysicallayer-list'),
            data,
            format='json'
        )
        #print("Below is the response.data")
        #print(response.data)    # {'name': ['This field may not be blank.']}

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_patch_ethernetphysicallayer_valid(self):
        '''
        UPDATE (PATCH) valid.
        '''
        epl1 = EthernetPhysicalLayer.objects.get(
            name = "EthernetPhysicalLayer 1"
        )
        data = {'name': 'EPL Y'}

        response = client.patch(
            reverse('apiv1:ethernetphysicallayer-detail', args=(epl1.id,)),
            data=json.dumps(data),
            content_type='application/json'
        )
        #print("This is the response:")
        #print(response)     # <Response status_code=200, "application/json">
        #print("This is the response.status_code:")
        #print(response.status_code)     # 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        epl = EthernetPhysicalLayer.objects.get(pk=epl1.id)
        response = client.get(
            reverse('apiv1:ethernetphysicallayer-detail',
            args=(epl.id,))
        )
        #print("This is the PATCHED response:")
        #print(response)     # <Response status_code=200, "application/json">

        #print("This is the PATCHED response.data:")
        #print(response.data)
        # {'abbreviation': 'manuY', 'name': 'EthernetPhysicalLayer 1', 'id': 8}
        serializer = EthernetPhysicalLayerSerializer(epl)
        self.assertEqual(response.data, serializer.data)


    def test_patch_ethernetphysicallayer_invalid(self):
        '''
        UPDATE (PATCH) invalid.
        '''
        epl1 = EthernetPhysicalLayer.objects.get(
            name = "EthernetPhysicalLayer 1"
        )
        data = {'name': ''}

        response = client.patch(
            reverse('apiv1:ethernetphysicallayer-detail', args=(epl1.id,)),
            data=json.dumps(data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_update_ethernetphysicallayer_valid(self):
        '''
        UPDATE (PUT) valid.
        '''
        epl1 = EthernetPhysicalLayer.objects.get(
            name = "EthernetPhysicalLayer 1"
        )
        data = {'name': 'EthernetPhysicalLayer Y'}

        response = client.put(
            reverse('apiv1:ethernetphysicallayer-detail', args=(epl1.id,)),
            data=json.dumps(data),
            content_type='application/json'
        )
        #print("This is the response:")
        #print(response)
        #print("This is the response.status_code:")
        #print(response.status_code)    # 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        epl = EthernetPhysicalLayer.objects.get(pk=epl1.id)
        response = client.get(
            reverse('apiv1:ethernetphysicallayer-detail',
            args=(epl.id,))
        )

        serializer = EthernetPhysicalLayerSerializer(epl)
        self.assertEqual(response.data, serializer.data)


    def test_update_ethernetphysicallayer_invalid(self):
        '''
        UPDATE (PUT) invalid.
        '''
        epl1 = EthernetPhysicalLayer.objects.get(
            name = "EthernetPhysicalLayer 1"
        )
        data = {'name': ''}

        response = client.put(
            reverse('apiv1:ethernetphysicallayer-detail', args=(epl1.id,)),
            data=json.dumps(data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_delete_ethernetphysicallayer_valid(self):
        '''
        Delete valid.
        '''
        epl1 = EthernetPhysicalLayer.objects.get(
            name = "EthernetPhysicalLayer 1"
        )

        response = client.delete(
            reverse('apiv1:ethernetphysicallayer-detail',
            args=(epl1.id,))
        )
        #print("This is the response:")
        #print(response)     # <Response status_code=204>
        #print("This is the response.status_code:")
        #print(response.status_code)     # 204

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_delete_ethernetphysicallayer_invalid(self):
        '''
        Delete invalid.
        '''
        epl_id = str(777)

        response = client.delete(
            reverse('apiv1:manufacturer-detail',
            args=(epl_id,))
        )
        #print("This is the response:")
        #print(response)     # <Response status_code=404, "application/json">
        #print("This is the response.status_code:")
        #print(response.status_code)     # 404

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

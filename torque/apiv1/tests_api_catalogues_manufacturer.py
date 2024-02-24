'''
This file does test:
 - List all Manufacturer objects.
 - Create, Read, Update (with the Put verb) and Delete a valid and an 
   invalid Manufacturer object. 
 - Update (with the Patch verb) a valid and an invalid Manufacturer object.


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
from .serializers import ManufacturerSerializer


# Instantiate Client. Will use this instance throught all the tests.
client = Client()


class APIManufacturerTest(TestCase):

    def setUp(self):
        '''
        Establish fixtures for each individual test case.
        '''
        Manufacturer.objects.create(
            name = "Manufacturer 1",
            abbreviation = "manu1",
        )
        m1 = Manufacturer.objects.get(abbreviation = "manu1")

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


    def test_list_all_manufacturers(self):
        '''
        List all objects.
        '''
        manufacturers = Manufacturer.objects.all()
        serializer = ManufacturerSerializer(manufacturers, many=True)

        response = client.get(reverse('apiv1:manufacturer-list'))

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_read_manufacturer_valid(self):
        '''
        READ valid.
        '''
        m = Manufacturer.objects.get(abbreviation = "manu1")
        serializer = ManufacturerSerializer(m)

        response = client.get(
            reverse('apiv1:manufacturer-detail', 
            args=(m.id,))
        )

        '''
        Verify that what we get through a HTTP request is the same than what
        the serializer provides.
        '''
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_read_manufacturer_invalid(self):
        '''
        READ invalid.
        '''
        m_id = str(777)

        response = client.get(
            reverse('apiv1:manufacturer-detail', 
            args=(m_id,))
        )
        #print(response.data)           # {'detail': 'Not found.'}
        #print(response.status_code)    # 404

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_create_manufacturer_valid(self):
        '''
        CREATE valid.
        '''
        data = {'name': 'Manufacturer X', 'abbreviation': 'manuX'}

        response = client.post(
            reverse('apiv1:manufacturer-list'), 
            data, 
            format='json'
        )

        m = Manufacturer.objects.get(name = data['name'])
        serializer = ManufacturerSerializer(m)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)


    def test_create_manufacturer_invalid(self):
        '''
        CREATE invalid.
        '''
        data = {'name': '', 'abbreviation': 'manuX'}

        response = client.post(
            reverse('apiv1:manufacturer-list'), 
            data, 
            format='json'
        )
        #print("Below is the response.data")
        #print(response.data)    # {'name': ['This field may not be blank.']}

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_patch_manufacturer_valid(self):
        '''
        UPDATE (PATCH) valid.
        '''
        m1 = Manufacturer.objects.get(abbreviation = "manu1")
        data = {'abbreviation': 'manuY'}

        response = client.patch(
            reverse('apiv1:manufacturer-detail', args=(m1.id,)),
            data=json.dumps(data),
            content_type='application/json'
        )
        #print("This is the response:")
        #print(response)     # <Response status_code=200, "application/json">
        #print("This is the response.status_code:")
        #print(response.status_code)     # 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        m = Manufacturer.objects.get(pk=m1.id)
        response = client.get(
            reverse('apiv1:manufacturer-detail', 
            args=(m.id,))
        )
        #print("This is the PATCHED response:")
        #print(response)
        # <Response status_code=200, "application/json">

        #print("This is the PATCHED response.data:")
        #print(response.data)   
        # {'abbreviation': 'manuY', 'name': 'Manufacturer 1', 'id': 8}
        serializer = ManufacturerSerializer(m)
        self.assertEqual(response.data, serializer.data)


    def test_patch_manufacturer_invalid(self):
        '''
        UPDATE (PATCH) invalid.
        '''
        m1 = Manufacturer.objects.get(abbreviation = "manu1")
        data = {'name': ''}

        response = client.patch(
            reverse('apiv1:manufacturer-detail', args=(m1.id,)),
            data=json.dumps(data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_update_manufacturer_valid(self):
        '''
        UPDATE (PUT) valid.
        '''
        m1 = Manufacturer.objects.get(abbreviation = "manu1")
        data = {'name': 'Manufacturer Y', 'abbreviation': 'manuY'}

        response = client.put(
            reverse('apiv1:manufacturer-detail', args=(m1.id,)),
            data=json.dumps(data),
            content_type='application/json'
        )
        #print("This is the response:")
        #print(response)
        #print("This is the response.status_code:")
        #print(response.status_code)    # 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        m = Manufacturer.objects.get(pk=m1.id)
        response = client.get(
            reverse('apiv1:manufacturer-detail',
            args=(m.id,))
        )

        serializer = ManufacturerSerializer(m)
        self.assertEqual(response.data, serializer.data)


    def test_update_manufacturer_invalid(self):
        '''
        UPDATE (PUT) invalid.
        '''
        m1 = Manufacturer.objects.get(abbreviation = "manu1")
        data = {'name': '', 'abbreviation': 'manuY'}

        response = client.put(
            reverse('apiv1:manufacturer-detail', args=(m1.id,)),
            data=json.dumps(data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_delete_manufacturer_valid(self):
        '''
        Delete valid.
        '''
        m1 = Manufacturer.objects.get(abbreviation = "manu1")

        response = client.delete(
            reverse('apiv1:manufacturer-detail',
            args=(m1.id,))
        )
        #print("This is the response:")
        #print(response)     # <Response status_code=204>
        #print("This is the response.status_code:")
        #print(response.status_code)     # 204

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_delete_manufacturer_invalid(self):
        '''
        Delete invalid.
        '''
        m_id = str(777)

        response = client.delete(
            reverse('apiv1:manufacturer-detail',
            args=(m_id,))
        )
        #print("This is the response:")
        #print(response)     # <Response status_code=404, "application/json">
        #print("This is the response.status_code:")
        #print(response.status_code)     # 404

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

'''
This file does test:
 - List all Manufacturer objects.
 - Create, Read, Update (with the Put verb) and Delete a valid and an 
   invalid Manufacturer object. 
 - Update (with the Patch verb) a valid and an invalid PartNumber object.


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
from .serializers import ManufacturerSerializer
from .serializers import PartNumberSerializer


# Instantiate Client. Will use this instance throught all the tests.
client = Client()


class APIPartNumberTest(TestCase):

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


    def test_list_all_partnumbers(self):
        '''
        List all objects.
        '''
        pns = PartNumber.objects.all()
        serializer = PartNumberSerializer(pns, many=True)

        response = client.get(reverse('apiv1:partnumber-list'))

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_read_partnumber_valid(self):
        '''
        READ valid.
        '''
        pn = PartNumber.objects.get(part_number = 'partnumber1')
        serializer = PartNumberSerializer(pn)

        response = client.get(
            reverse('apiv1:partnumber-detail', 
            args=(pn.id,))
        )

        '''
        Verify that what we get through a HTTP request is the same than what
        the serializer provides.
        '''
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_read_partnumber_invalid(self):
        '''
        READ invalid.
        '''
        pn_id = str(777)

        response = client.get(
            reverse('apiv1:partnumber-detail', 
            args=(pn_id,))
        )
        #print(response.data)           # {'detail': 'Not found.'}
        #print(response.status_code)    # 404

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_create_partnumber_valid(self):
        '''
        CREATE valid.
        '''
        m1 = Manufacturer.objects.get(abbreviation = "manu1")
        data = {
            'part_number': 'partnumberX',
            'description': 'partnumberX description',
            'manufacturer': m1.id
        }

        response = client.post(
            reverse('apiv1:partnumber-list'),
            data,
            format='json'
        )

        pn = PartNumber.objects.get(part_number = data['part_number'])
        serializer = PartNumberSerializer(pn)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)


    def test_create_partnumber_invalid(self):
        '''
        CREATE invalid.
        '''
        m1 = Manufacturer.objects.get(abbreviation = "manu1")
        data = {
            'partnumber': '',
            'description': 'partnumberX description',
            'manufacturer': m1.id
        }

        response = client.post(
            reverse('apiv1:partnumber-list'), 
            data, 
            format='json'
        )
        #print("Below is the response.data")
        #print(response.data)    # {'name': ['This field may not be blank.']}

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_patch_partnumber_valid(self):
        '''
        UPDATE (PATCH) valid.
        '''
        pn1 = PartNumber.objects.get(part_number = 'partnumber1')
        data = {'part_number': 'partnumberY'}

        response = client.patch(
            reverse('apiv1:partnumber-detail', args=(pn1.id,)),
            data=json.dumps(data),
            content_type='application/json'
        )
        #print("This is the response:")
        #print(response)     # <Response status_code=200, "application/json">
        #print("This is the response.status_code:")
        #print(response.status_code)     # 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        pn = PartNumber.objects.get(pk=pn1.id)
        response = client.get(
            reverse('apiv1:partnumber-detail',
            args=(pn.id,))
        )
        #print("This is the PATCHED response:")
        #print(response)
        # <Response status_code=200, "application/json">

        #print("This is the PATCHED response.data:")
        #print(response.data)   
        # {'abbreviation': 'manuY', 'name': 'Manufacturer 1', 'id': 8}
        serializer = PartNumberSerializer(pn)
        self.assertEqual(response.data, serializer.data)


    def test_patch_partnumber_invalid(self):
        '''
        UPDATE (PATCH) invalid.
        '''
        pn = PartNumber.objects.get(part_number = 'partnumber1')
        data = {'part_number': ''}

        response = client.patch(
            reverse('apiv1:partnumber-detail', args=(pn.id,)),
            data=json.dumps(data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_update_partnumber_valid(self):
        '''
        UPDATE (PUT) valid.
        '''
        m1 = Manufacturer.objects.get(abbreviation = "manu1")
        pn1 = PartNumber.objects.get(part_number = 'partnumber1')
        data = {
            'part_number': 'partnumberY',
            'description': 'partnumberY description',
            'manufacturer': m1.id
        }

        response = client.put(
            reverse('apiv1:partnumber-detail', args=(pn1.id,)),
            data=json.dumps(data),
            content_type='application/json'
        )
        #print("This is the response:")
        #print(response)
        #print("This is the response.status_code:")
        #print(response.status_code)    # 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        pn = PartNumber.objects.get(pk=pn1.id)
        response = client.get(
            reverse('apiv1:partnumber-detail',
            args=(pn.id,))
        )

        serializer = PartNumberSerializer(pn)
        self.assertEqual(response.data, serializer.data)


    def test_update_partnumber_invalid(self):
        '''
        UPDATE (PUT) invalid.
        '''
        pn1 = PartNumber.objects.get(part_number = 'partnumber1')
        data = {
            'part_number': '',
            'description': 'partnumber1 description',
            'manufacturer': pn1.id
        }

        response = client.put(
            reverse('apiv1:partnumber-detail', args=(pn1.id,)),
            data=json.dumps(data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_delete_partnumber_valid(self):
        '''
        Delete valid.
        '''
        pn1 = PartNumber.objects.get(part_number = 'partnumber1')

        response = client.delete(
            reverse('apiv1:partnumber-detail',
            args=(pn1.id,))
        )
        #print("This is the response:")
        #print(response)     # <Response status_code=204>
        #print("This is the response.status_code:")
        #print(response.status_code)     # 204

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_delete_partnumber_invalid(self):
        '''
        Delete invalid.
        '''
        pn_id = str(777)

        response = client.delete(
            reverse('apiv1:partnumber-detail',
            args=(pn_id,))
        )
        #print("This is the response:")
        #print(response)     # <Response status_code=404, "application/json">
        #print("This is the response.status_code:")
        #print(response.status_code)     # 404

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

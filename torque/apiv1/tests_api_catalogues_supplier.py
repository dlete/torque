'''
This file does test:
 - List all Manufacturer objects.
 - Create, Read, Update (with the Put verb) and Delete a valid and an
   invalid Manufacturer object.
 - Update (with the Patch verb) a valid and an invalid Supplier object.

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
from catalogues.models import Supplier
from .serializers import SupplierSerializer


# Instantiate Client. Will use this instance throught all the tests.
client = Client()


class APISupplierTest(TestCase):

    def setUp(self):
        '''
        Establish fixtures for each individual test case.
        '''
        Supplier.objects.create(
            name = "Supplier 1",
            abbreviation = "sup1",
        )
        s1 = Supplier.objects.get(abbreviation = "sup1")

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


    def test_list_suppliers(self):
        '''
        List all objects.
        '''
        suppliers = Supplier.objects.all()
        serializer = SupplierSerializer(suppliers, many=True)

        response = client.get(reverse('apiv1:supplier-list'))

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_read_supplier_valid(self):
        '''
        READ valid.
        '''
        s = Supplier.objects.get(abbreviation = "sup1")
        serializer = SupplierSerializer(s)

        response = client.get(reverse('apiv1:supplier-detail', args=(s.id,)))

        '''
        Verify that what we get through a HTTP request is the same than what
        the serializer provides.
        '''
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_read_supplier_invalid(self):
        '''
        READ invalid.
        '''
        s_id = str(777)

        response = client.get(reverse('apiv1:supplier-detail', args=(s_id,)))
        #print(response.data)           # {'detail': 'Not found.'}
        #print(response.status_code)    # 404

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_create_supplier_valid(self):
        '''
        CREATE valid.
        '''
        data = {'name': 'Supplier X', 'abbreviation': 'supX'}

        response = client.post(
            reverse('apiv1:supplier-list'),
            data,
            format='json'
        )

        s = Supplier.objects.get(name = data['name'])
        serializer = SupplierSerializer(s)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)


    def test_create_supplier_invalid(self):
        '''
        CREATE invalid.
        '''
        data = {'name': '', 'abbreviation': 'supX'}

        response = client.post(
            reverse('apiv1:supplier-list'),
            data,
            format='json'
        )
        #print("Below is the response.data")
        #print(response.data)    # {'name': ['This field may not be blank.']}

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_patch_supplier_valid(self):
        '''
        UPDATE (PATCH) valid.
        '''
        s1 = Supplier.objects.get(abbreviation = "sup1")
        data = {'abbreviation': 'supY'}

        response = client.patch(
            reverse('apiv1:supplier-detail', args=(s1.id,)), 
            data=json.dumps(data),
            content_type='application/json'
        )
        #print("This is the response:")
        #print(response)     # <Response status_code=200, "application/json">
        #print("This is the response.status_code:")
        #print(response.status_code)     # 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        s = Supplier.objects.get(pk=s1.id)
        response = client.get(reverse('apiv1:supplier-detail', args=(s.id,)))
        #print("This is the PATCHED response:")
        #print(response)     # <Response status_code=200, "application/json">
        #print("This is the PATCHED response.data:")

        #print(response.data)   
        # {'abbreviation': 'supY', 'name': 'Supplier 1', 'id': 8}

        serializer = SupplierSerializer(s)
        self.assertEqual(response.data, serializer.data)


    def test_patch_supplier_invalid(self):
        '''
        UPDATE (PATCH) invalid.
        '''
        s1 = Supplier.objects.get(abbreviation = "sup1")
        data = {'name': ''}

        response = client.patch(
            reverse('apiv1:supplier-detail', args=(s1.id,)),
            data=json.dumps(data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_update_supplier_valid(self):
        '''
        UPDATE (PUT) valid.
        '''
        s1 = Supplier.objects.get(abbreviation = "sup1")
        data = {'name': 'Supplier Y', 'abbreviation': 'supY'}

        response = client.put(
            reverse('apiv1:supplier-detail', args=(s1.id,)),
            data=json.dumps(data),
            content_type='application/json'
        )
        #print("This is the response:")
        #print(response)
        #print("This is the response.status_code:")
        #print(response.status_code)    # 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        s = Supplier.objects.get(pk=s1.id)
        response = client.get(reverse('apiv1:supplier-detail', args=(s.id,)))
        serializer = SupplierSerializer(s)
        self.assertEqual(response.data, serializer.data)


    def test_update_supplier_invalid(self):
        '''
        UPDATE (PUT) invalid.
        '''
        s1 = Supplier.objects.get(abbreviation = "sup1")
        data = {'name': '', 'abbreviation': 'supY'}

        response = client.put(
            reverse('apiv1:supplier-detail', args=(s1.id,)),
            data=json.dumps(data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_delete_supplier_valid(self):
        '''
        Delete valid.
        '''
        s1 = Supplier.objects.get(abbreviation = "sup1")

        response = client.delete(
            reverse('apiv1:supplier-detail', args=(s1.id,))
        )
        #print("This is the response:")
        #print(response)     # <Response status_code=204>
        #print("This is the response.status_code:")
        #print(response.status_code)     # 204

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_delete_supplier_invalid(self):
        '''
        Delete invalid.
        '''
        s_id = str(777)

        response = client.delete(
            reverse('apiv1:supplier-detail', args=(s_id,))
        )
        #print("This is the response:")
        #print(response)     # <Response status_code=404, "application/json">
        #print("This is the response.status_code:")
        #print(response.status_code)     # 404

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

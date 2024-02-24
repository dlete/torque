'''
This file does test the Circuit class of the inventories app:
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
from catalogues.models import Supplier
from inventories.models import Circuit
#from .serializers import SupplierSerializer
from .serializers import CircuitSerializer

# Instantiate Client. Will use this instance throught all the tests.
client = Client()


class APICircuitTest(TestCase):

    def setUp(self):
        '''
        Establish fixtures for each individual test case.
        '''
        Supplier.objects.create(
            name = 'Supplier 1',
            abbreviation = 'sup1',
        )
        s1 = Supplier.objects.get(abbreviation = "sup1")
        
        Circuit.objects.create(
            supplier = s1,
            circuit_id = 'cid1234',
            a_end_description = 'c1_a_end_desc',
            b_end_description = 'c1_b_end_desc',
            circuit_type = 'managed',
            circuit_info = 'purchased on 13 March 1492',
        )
        c1 = Circuit.objects.get(circuit_id = 'cid1234')

        user = User.objects.create_superuser(
            username='admin',
            password='1234',
            email='demo@demo.com',
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


    def test_list_all_circuits(self):
        '''
        List all objects.
        '''
        circuits = Circuit.objects.all()
        serializer = CircuitSerializer(circuits, many=True)

        response = client.get(reverse('apiv1:circuit-list'))

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_read_circuit_valid(self):
        '''
        READ valid.
        '''
        c1 = Circuit.objects.get(circuit_id = 'cid1234')

        serializer = CircuitSerializer(c1)
        response = client.get(
            reverse('apiv1:circuit-detail', args=(c1.id,))
        )

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_read_circuit_invalid(self):
        '''
        READ invalid.
        '''
        c_id = str(777)

        response = client.get(
            reverse('apiv1:circuit-detail', args=(c_id,))
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_create_circuit_valid(self):
        '''
        CREATE valid.
        '''
        s1 = Supplier.objects.get(abbreviation = "sup1")
        data = {
            'supplier': s1.id,
            'circuit_id': 'cidXXXX',
            'a_end_description': 'cX_a_end_desc',
            'b_end_description': 'cX_b_end_desc',
            'circuit_type': 'managed',
            'circuit_info': 'purchased on 13 March 1492',
        }
        response = client.post(
            reverse('apiv1:circuit-list'),
            data,
            format='json'
        )

        c1 = Circuit.objects.get(circuit_id = 'cidXXXX')
        serializer = CircuitSerializer(c1)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)


    def test_create_circuit_invalid(self):
        '''
        CREATE invalid.
        '''
        s1 = Supplier.objects.get(abbreviation = "sup1")
        data = {
            'supplier': s1,
            'circuit_id': '',
            'a_end_description': 'cX_a_end_desc',
            'b_end_description': 'cX_b_end_desc',
            'circuit_type': 'managed',
            'circuit_info': 'purchased on 13 March 1492',
        }
        response = client.post(
            reverse('apiv1:circuit-list'),
            data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_patch_circuit_valid(self):
        '''
        UPDATE (PATCH) valid.
        '''
        c1 = Circuit.objects.get(circuit_id = 'cid1234')
        data = {
            'circuit_id': 'cidYYYY',
            'a_end_description': 'cY_a_end_desc',
            'b_end_description': 'cY_b_end_desc',
            'circuit_type': 'managed',
        }
        response = client.patch(
            reverse('apiv1:circuit-detail', args=(c1.id,)),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        c = Circuit.objects.get(pk = c1.id)
        response = client.get(
            reverse('apiv1:circuit-detail', args=(c.id,)),
        )
        serializer = CircuitSerializer(c)
        self.assertEqual(response.data, serializer.data)


    def test_patch_circuit_invalid(self):
        '''
        UPDATE (PATCH) invalid.
        '''
        c1 = Circuit.objects.get(circuit_id = 'cid1234')
        data = {
            'circuit_id': '',
            'a_end_description': 'cY_a_end_desc',
            'b_end_description': 'cY_b_end_desc',
            'circuit_type': 'managed',
        }
        response = client.patch(
            reverse('apiv1:circuit-detail', args=(c1.id,)),
            data=json.dumps(data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_update_circuit_valid(self):
        '''
        UPDATE (PUT) valid.
        '''
        s1 = Supplier.objects.get(abbreviation = "sup1")
        c1 = Circuit.objects.get(circuit_id = 'cid1234')
        data = {
            'supplier': s1.id,
            'circuit_id': 'cid1234',
            'a_end_description': 'cY_a_end_desc',
            'b_end_description': 'cY_b_end_desc',
            'circuit_type': 'managed wireless',
            'circuit_info': 'purchased on 33 March 1001',
        }
        response = client.put(
            reverse('apiv1:circuit-detail', args=(c1.id,)),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        response = client.get(
            reverse('apiv1:circuit-detail', args=(c1.id,)),
        )
        c = Circuit.objects.get(pk = c1.id)
        serializer = CircuitSerializer(c)
        self.assertEqual(response.data, serializer.data)


    def test_update_circuit_invalid(self):
        '''
        UPDATE (PUT) invalid.
        '''
        s1 = Supplier.objects.get(abbreviation = "sup1")
        c1 = Circuit.objects.get(circuit_id = 'cid1234')
        data = {
            'supplier': s1.id,
            'circuit_id': '',
            'a_end_description': 'cY_a_end_desc',
            'b_end_description': 'cY_b_end_desc',
            'circuit_type': 'managed wireless',
            'circuit_info': 'purchased on 33 March 1001',
        }
        response = client.put(
            reverse('apiv1:circuit-detail', args=(c1.id,)),
            data=json.dumps(data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_delete_circuit_valid(self):
        '''
        Delete valid.
        '''
        c1 = Circuit.objects.get(circuit_id = 'cid1234')
        response = client.delete(
            reverse('apiv1:circuit-detail',
            args=(c1.id,))
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_delete_circuit_invalid(self):
        '''
        Delete invalid.
        '''
        c_id = str(777)
        response = client.delete(
            reverse('apiv1:circuit-detail',
            args=(c_id,))
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


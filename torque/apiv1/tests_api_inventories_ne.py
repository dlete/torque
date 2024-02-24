'''
This file does test the Ne class of the inventories app:
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
from inventories.models import Ne
from inventories.models import OsCredential
from .serializers import NeSerializer

# Instantiate Client. Will use this instance throught all the tests.
client = Client()


class APINeTest(TestCase):

    def setUp(self):
        '''
        Establish fixtures for each individual test case.
        '''
        OsCredential.objects.create(
            username = 'os_credential1',
            password = 'os_credential1_password',
        )
        osc1 = OsCredential.objects.get(username = 'os_credential1')

        Ne.objects.create(
            fqdn = 'fqdn1',
            os_credential = osc1,
        )
        ne1 = Ne.objects.get(fqdn = 'fqdn1')
        
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


    def test_list_all_nes(self):
        '''
        List all objects.
        '''
        nes = Ne.objects.all()
        serializer = NeSerializer(nes, many=True)

        response = client.get(reverse('apiv1:ne-list'))

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_read_ne_valid(self):
        '''
        READ valid.
        '''
        ne1 = Ne.objects.get(fqdn = 'fqdn1')

        serializer = NeSerializer(ne1)
        response = client.get(
            reverse('apiv1:ne-detail', args=(ne1.id,))
        )

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_read_ne_invalid(self):
        '''
        READ invalid.
        '''
        ne_id = str(777)

        response = client.get(
            reverse('apiv1:ne-detail', args=(ne_id,))
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_create_ne_valid(self):
        '''
        CREATE valid.
        '''
        osc1 = OsCredential.objects.get(username = 'os_credential1')
        data = {
            'fqdn': 'fqdnX',
            'os_credential': osc1.id,
        }
        response = client.post(
            reverse('apiv1:ne-list'),
            data,
            format='json'
        )

        ne1 = Ne.objects.get(fqdn = 'fqdnX')
        serializer = NeSerializer(ne1)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)


    def test_create_ne_invalid(self):
        '''
        CREATE invalid.
        '''
        osc1 = OsCredential.objects.get(username = 'os_credential1')
        data = {
            'fqdn': '',
            'os_credential': osc1.id,
        }
        response = client.post(
            reverse('apiv1:ne-list'),
            data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_patch_ne_valid(self):
        '''
        UPDATE (PATCH) valid.
        '''
        osc1 = OsCredential.objects.get(username = 'os_credential1')
        ne1 = Ne.objects.get(fqdn = 'fqdn1')
        data = {
            'fqdn': 'fqdnY',
            'os_credential': osc1.id,
        }
        response = client.patch(
            reverse('apiv1:ne-detail', args=(ne1.id,)),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        ne = Ne.objects.get(pk = ne1.id)
        response = client.get(
            reverse('apiv1:ne-detail', args=(ne.id,)),
        )
        serializer = NeSerializer(ne)
        self.assertEqual(response.data, serializer.data)


    def test_patch_ne_invalid(self):
        '''
        UPDATE (PATCH) invalid.
        '''
        osc1 = OsCredential.objects.get(username = 'os_credential1')
        ne1 = Ne.objects.get(fqdn = 'fqdn1')
        data = {
            'fqdn': '',
            'os_credential': osc1.id,
        }
        response = client.patch(
            reverse('apiv1:ne-detail', args=(ne1.id,)),
            data=json.dumps(data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_update_ne_valid(self):
        '''
        UPDATE (PUT) valid.
        '''
        osc1 = OsCredential.objects.get(username = 'os_credential1')
        ne1 = Ne.objects.get(fqdn = 'fqdn1')
        data = {
            'fqdn': 'fqdnX',
            'os_credential': osc1.id,
        }
        response = client.put(
            reverse('apiv1:ne-detail', args=(ne1.id,)),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        response = client.get(
            reverse('apiv1:ne-detail', args=(ne1.id,)),
        )
        ne = Ne.objects.get(pk = ne1.id)
        serializer = NeSerializer(ne)
        self.assertEqual(response.data, serializer.data)


    def test_update_ne_invalid(self):
        '''
        UPDATE (PUT) invalid.
        '''
        osc1 = OsCredential.objects.get(username = 'os_credential1')
        ne1 = Ne.objects.get(fqdn = 'fqdn1')
        data = {
            'fqdn': '',
            'os_credential': osc1.id,
        }
        response = client.put(
            reverse('apiv1:ne-detail', args=(ne1.id,)),
            data=json.dumps(data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_delete_ne_valid(self):
        '''
        Delete valid.
        '''
        ne1 = Ne.objects.get(fqdn = 'fqdn1')
        response = client.delete(
            reverse('apiv1:ne-detail',
            args=(ne1.id,))
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_delete_ne_invalid(self):
        '''
        Delete invalid.
        '''
        ne_id = str(777)
        response = client.delete(
            reverse('apiv1:ne-detail',
            args=(ne_id,))
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


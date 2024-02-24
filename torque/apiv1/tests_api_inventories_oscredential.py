'''
This file does test the OsCredential class of the inventories app:
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
from inventories.models import OsCredential
from .serializers import OsCredentialSerializer

# Instantiate Client. Will use this instance throught all the tests.
client = Client()


class APIOsCredentialTest(TestCase):

    def setUp(self):
        '''
        Establish fixtures for each individual test case.
        '''
        OsCredential.objects.create(
            username = 'os_credential1',
            password = 'os_credential1_password'
        )
        osc1 = OsCredential.objects.get(username = 'os_credential1')

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


    def test_list_all_oscredentials(self):
        '''
        List all objects.
        '''
        oscs = OsCredential.objects.all()
        serializer = OsCredentialSerializer(oscs, many=True)

        response = client.get(reverse('apiv1:oscredential-list'))

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_read_oscredential_valid(self):
        '''
        READ valid.
        '''
        osc1 = OsCredential.objects.get(username = 'os_credential1')

        serializer = OsCredentialSerializer(osc1)
        response = client.get(
            reverse('apiv1:oscredential-detail', args=(osc1.id,))
        )

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_read_oscredential_invalid(self):
        '''
        READ invalid.
        '''
        osc_id = str(777)

        response = client.get(
            reverse('apiv1:oscredential-detail', args=(osc_id,))
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_create_oscredential_valid(self):
        '''
        CREATE valid.
        '''
        data = {
            'username': 'os_credentialX',
            'password': 'os_credentialX_password'
        }
        response = client.post(
            reverse('apiv1:oscredential-list'),
            data,
            format='json'
        )

        osc = OsCredential.objects.get(username = 'os_credentialX')
        serializer = OsCredentialSerializer(osc)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)


    def test_create_oscredential_invalid(self):
        '''
        CREATE invalid.
        '''
        data = {
            'username': '',
            'password': 'os_credentialY_password'
        }
        response = client.post(
            reverse('apiv1:oscredential-list'),
            data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_patch_oscredential_valid(self):
        '''
        UPDATE (PATCH) valid.
        '''
        osc1 = OsCredential.objects.get(username = 'os_credential1')
        data = {
            'password': 'os_credentialY_password',
        }

        response = client.patch(
            reverse('apiv1:oscredential-detail', args=(osc1.id,)),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        osc = OsCredential.objects.get(pk = osc1.id)
        response = client.get(
            reverse('apiv1:oscredential-detail', args=(osc.id,)),
        )
        serializer = OsCredentialSerializer(osc)
        self.assertEqual(response.data, serializer.data)


    def test_patch_oscredential_invalid(self):
        '''
        UPDATE (PATCH) invalid.
        '''
        osc1 = OsCredential.objects.get(username = 'os_credential1')
        data = {
            'username': '',
            'password': 'os_credentialY_password',
        }
        response = client.patch(
            reverse('apiv1:oscredential-detail', args=(osc1.id,)),
            data=json.dumps(data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_update_oscredential_valid(self):
        '''
        UPDATE (PUT) valid.
        '''
        osc1 = OsCredential.objects.get(username = 'os_credential1')
        data = {
            'username': 'os_credential1',
            'password': 'os_credentialY_password',
        }
        response = client.put(
            reverse('apiv1:oscredential-detail', args=(osc1.id,)),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        osc = OsCredential.objects.get(pk = osc1.id)
        response = client.get(
            reverse('apiv1:oscredential-detail', args=(osc1.id,)),
        )
        serializer = OsCredentialSerializer(osc)
        self.assertEqual(response.data, serializer.data)


    def test_update_oscredential_invalid(self):
        '''
        UPDATE (PUT) invalid.
        '''
        osc1 = OsCredential.objects.get(username = 'os_credential1')
        data = {
            'username': '',
            'password': 'os_credentialY_password',
        }
        response = client.put(
            reverse('apiv1:oscredential-detail', args=(osc1.id,)),
            data=json.dumps(data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_delete_oscredential_valid(self):
        '''
        Delete valid.
        '''
        osc1 = OsCredential.objects.get(username = 'os_credential1')
        response = client.delete(
            reverse('apiv1:oscredential-detail',
            args=(osc1.id,))
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_delete_oscredential_invalid(self):
        '''
        Delete invalid.
        '''
        osc_id = str(777)
        response = client.delete(
            reverse('apiv1:oscredential-detail',
            args=(osc_id,))
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


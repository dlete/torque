'''
This file does test the API calls to the Os class:
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
from catalogues.models import Os
from .serializers import OsSerializer


# Instantiate Client. Will use this instance throught all the tests.
client = Client()


class APIOsTest(TestCase):

    def setUp(self):
        '''
        Establish fixtures for each individual test case.
        '''
        Manufacturer.objects.create(
            name = 'Manufacturer 1',
            abbreviation = 'manu1',
        )
        m1 = Manufacturer.objects.get(abbreviation = 'manu1')

        Os.objects.create(
            manufacturer = m1,
            family = 'os_family1',
            version = 'os_version1'
        )
        os1 = Os.objects.get(
            manufacturer = m1,
            family = 'os_family1',
            version = 'os_version1'
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


    def test_list_all_os(self):
        '''
        List all objects.
        '''
        oss = Os.objects.all()
        serializer = OsSerializer(oss, many=True)

        response = client.get(reverse('apiv1:os-list'))

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_read_os_valid(self):
        '''
        READ valid.
        '''
        m1 = Manufacturer.objects.get(abbreviation = 'manu1')
        os1 = Os.objects.get(
            manufacturer = m1,
            family = "os_family1",
            version = "os_version1"
        )

        serializer = OsSerializer(os1)
        response = client.get(
            reverse('apiv1:os-detail',
            args=(os1.id,))
        )

        '''
        Verify that what we get through a HTTP request is the same than what
        the serializer provides.
        '''
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_read_os_invalid(self):
        '''
        READ invalid.
        '''
        os_id = str(777)

        response = client.get(
            reverse('apiv1:os-detail',
            args=(os_id,))
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_create_os_valid(self):
        '''
        CREATE valid.
        '''
        m1 = Manufacturer.objects.get(abbreviation = 'manu1')
        data = {
            'manufacturer': m1.id,
            'family': 'os_family_X',
            'version': 'os_version_XX'
        }

        response = client.post(
            reverse('apiv1:os-list'),
            data,
            format='json'
        )

        os = Os.objects.get(
            manufacturer = m1.id,
            family = 'os_family_X',
            version = 'os_version_XX'
        )
        serializer = OsSerializer(os)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)


    def test_create_os_invalid(self):
        '''
        CREATE invalid.
        '''
        data = {
            'manufacturer': '',
            'family': '',
            'version': '' 
        }
        response = client.post(
            reverse('apiv1:os-list'),
            data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_patch_os_valid(self):
        '''
        UPDATE (PATCH) valid.
        '''
        m1 = Manufacturer.objects.get(abbreviation = 'manu1')
        os1 = Os.objects.get(
            manufacturer = m1,
            family = 'os_family1',
            version = 'os_version1'
        )
        data = {
            'family': 'os_familyY'
        }

        response = client.patch(
            reverse('apiv1:os-detail', args=(os1.id,)),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        os = Os.objects.get(pk=os1.id)
        response = client.get(
            reverse('apiv1:os-detail',
            args=(os.id,))
        )

        serializer = OsSerializer(os)
        self.assertEqual(response.data, serializer.data)


    def test_patch_os_invalid(self):
        '''
        UPDATE (PATCH) invalid.
        '''
        m1 = Manufacturer.objects.get(abbreviation = 'manu1')
        os1 = Os.objects.get(
            manufacturer = m1.id,
            family = 'os_family1',
            version = 'os_version1'
        )
        data = {
            'family': ''
        }

        response = client.patch(
            reverse('apiv1:os-detail', args=(os1.id,)),
            data=json.dumps(data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_update_os_valid(self):
        '''
        UPDATE (PUT) valid.
        '''
        m1 = Manufacturer.objects.get(abbreviation = 'manu1')
        os1 = Os.objects.get(
            manufacturer = m1,
            family = 'os_family1',
            version = 'os_version1'
        )
        data = {
            'manufacturer': m1.id,
            'family': 'os_familyY',
            'version': 'os_versionY'
        }
        response = client.put(
            reverse('apiv1:os-detail', args=(os1.id,)),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        os = Os.objects.get(pk=os1.id)
        response = client.get(
            reverse('apiv1:os-detail',
            args=(os.id,))
        )
        serializer = OsSerializer(os)
        self.assertEqual(response.data, serializer.data)


    def test_update_os_invalid(self):
        '''
        UPDATE (PUT) invalid.
        '''
        m1 = Manufacturer.objects.get(abbreviation = 'manu1')
        os1 = Os.objects.get(
            manufacturer = m1,
            family = 'os_family1',
            version = 'os_version1'
        )
        data = {
            'manufacturer': '',
            'family': 'os_familyY',
            'version': 'os_versionY'
        }

        response = client.put(
            reverse('apiv1:os-detail', args=(os1.id,)),
            data=json.dumps(data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_delete_os_valid(self):
        '''
        Delete valid.
        '''
        m1 = Manufacturer.objects.get(abbreviation = 'manu1')
        os1 = Os.objects.get(
            manufacturer = m1,
            family = 'os_family1',
            version = 'os_version1'
        )
        response = client.delete(
            reverse('apiv1:os-detail',
            args=(os1.id,))
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_delete_partnumber_invalid(self):
        '''
        Delete invalid.
        '''
        os_id = str(777)
        response = client.delete(
            reverse('apiv1:os-detail',
            args=(os_id,))
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

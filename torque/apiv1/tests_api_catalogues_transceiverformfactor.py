'''
This file does test the TransceiverFormFactor class:
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
from catalogues.models import TransceiverFormFactor
from .serializers import TransceiverFormFactorSerializer


# Instantiate Client. Will use this instance throught all the tests.
client = Client()


class APITransceiverFormFactorTest(TestCase):

    def setUp(self):
        '''
        Establish fixtures for each individual test case.
        '''
        TransceiverFormFactor.objects.create(
            name = "TransceiverFF1",
            description = "TransceiverFF1 description"
        )
        ttf1 = TransceiverFormFactor.objects.get(name = "TransceiverFF1")

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


    def test_list_all_transceiverffs(self):
        '''
        List all objects.
        '''
        ttfs = TransceiverFormFactor.objects.all()
        serializer = TransceiverFormFactorSerializer(ttfs, many=True)

        response = client.get(reverse('apiv1:transceiverformfactor-list'))

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_read_transceiverformfactor_valid(self):
        '''
        READ valid.
        '''
        ttf = TransceiverFormFactor.objects.get(name = "TransceiverFF1")
        serializer = TransceiverFormFactorSerializer(ttf)

        response = client.get(
            reverse('apiv1:transceiverformfactor-detail',
            args=(ttf.id,))
        )

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_read_transceiverformfactor_invalid(self):
        '''
        READ invalid.
        '''
        ttf_id = str(777)

        response = client.get(
            reverse('apiv1:transceiverformfactor-detail',
            args=(ttf_id,))
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_create_transceiverformfactor_valid(self):
        '''
        CREATE valid.
        '''
        data = {
            'name': 'TransceiverFFX', 
            'description': 'TransceiverFFX description'
        }

        response = client.post(
            reverse('apiv1:transceiverformfactor-list'),
            data,
            format='json'
        )

        ttf = TransceiverFormFactor.objects.get(name = data['name'])
        serializer = TransceiverFormFactorSerializer(ttf)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)


    def test_create_transceiverformfactor_invalid(self):
        '''
        CREATE invalid.
        '''
        data = {
            'name': '', 
            'description': 'TransceiverFFX description'
        }

        response = client.post(
            reverse('apiv1:transceiverformfactor-list'),
            data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_patch_transceiverformfactor_valid(self):
        '''
        UPDATE (PATCH) valid.
        '''
        ttf1 = TransceiverFormFactor.objects.get(name = "TransceiverFF1")
        data = {
            'description': 'TransceiverFFX description'
        }
        response = client.patch(
            reverse('apiv1:transceiverformfactor-detail', args=(ttf1.id,)),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        ttf = TransceiverFormFactor.objects.get(pk=ttf1.id)
        response = client.get(
            reverse('apiv1:transceiverformfactor-detail',
            args=(ttf.id,))
        )
        serializer = TransceiverFormFactorSerializer(ttf)
        self.assertEqual(response.data, serializer.data)


    def test_patch_transceiverformfactor_invalid(self):
        '''
        UPDATE (PATCH) invalid.
        '''
        ttf1 = TransceiverFormFactor.objects.get(name = "TransceiverFF1")
        data = {'name': ''}

        response = client.patch(
            reverse('apiv1:transceiverformfactor-detail', args=(ttf1.id,)),
            data=json.dumps(data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_update_transceiverformfactor_valid(self):
        '''
        UPDATE (PUT) valid.
        '''
        ttf1 = TransceiverFormFactor.objects.get(name = "TransceiverFF1")
        data = {
            'name': 'TransceiverFFY',
            'description': 'TransceiverFFY description'
        }
        response = client.put(
            reverse('apiv1:transceiverformfactor-detail', args=(ttf1.id,)),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        ttf = TransceiverFormFactor.objects.get(pk=ttf1.id)
        response = client.get(
            reverse('apiv1:transceiverformfactor-detail',
            args=(ttf.id,))
        )
        serializer = TransceiverFormFactorSerializer(ttf)
        self.assertEqual(response.data, serializer.data)


    def test_update_transceiverformfactor_invalid(self):
        '''
        UPDATE (PUT) invalid.
        '''
        ttf1 = TransceiverFormFactor.objects.get(name = "TransceiverFF1")
        data = {
            'name': '', 
            'description': 'TransceiverFFY description'
        }
        response = client.put(
            reverse('apiv1:transceiverformfactor-detail', args=(ttf1.id,)),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_delete_transceiverformfactor_valid(self):
        '''
        Delete valid.
        '''
        #m1 = Manufacturer.objects.get(abbreviation = "manu1")
        ttf1 = TransceiverFormFactor.objects.get(name = "TransceiverFF1")
        response = client.delete(
            reverse('apiv1:transceiverformfactor-detail',
            args=(ttf1.id,))
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_delete_transceiverformfactor_invalid(self):
        '''
        Delete invalid.
        '''
        ttf_id = str(777)

        response = client.delete(
            reverse('apiv1:transceiverformfactor-detail',
            args=(ttf_id,))
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

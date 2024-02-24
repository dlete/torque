# Core Django imports
from django.test import TestCase
from django.urls import reverse

# This project apps imports
from .models import Ne
from .models import OsCredential


class InventoryViewsTests(TestCase):

    def setUp(self):
        '''
        Establish fixtures for each individual test case.
        '''
        OsCredential.objects.create(
            username="test_username1",
            password="test_password1",
        )
        osc1 = OsCredential.objects.get(username="test_username1")

        Ne.objects.create(
            fqdn="ne1.acme.net",
            os_credential=osc1,
        )
        ne1 = Ne.objects.get(fqdn="ne1.acme.net")


    def test_ne_list(self):
        '''
        Test Inventory view ne_list.
        '''
        response = self.client.get(reverse('inventories:ne_list'))
        self.assertEqual(response.status_code, 200)
        #self.assertContains(response, "You know why you are here. HIT ME!!")
        self.assertContains(response, "HIT ME")
        self.assertQuerysetEqual(
            response.context['ne_all'], 
            [repr(ne) for ne in Ne.objects.all()]
        )


    def test_ne_detail(self):
        '''
        Test Inventory view ne_detail.
        '''
        ne = Ne.objects.get(fqdn="ne1.acme.net")
        '''use inventories:<"name"> in inventories/urls.py>'''
        url = reverse('inventories:ne_detail', args=(ne.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Details for")
        self.assertContains(response, "Details for " + ne.fqdn)
        

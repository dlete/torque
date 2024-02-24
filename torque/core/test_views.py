# Core Django imports
from django.test import TestCase
from django.urls import reverse


class CoreViewsTests(TestCase):

    def test_core_about(self):
        '''
        Test Core view about.
        '''
        response = self.client.get(reverse('core:about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Torquemada")

    def test_core_features(self):
        '''
        Test Core view features.
        '''
        response = self.client.get(reverse('core:features'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "These are the items the tool will audit"
        )

    def test_core_known_bugs(self):
        '''
        Test Core view known_bugs.
        '''
        response = self.client.get(reverse('core:known_bugs'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "These are the known bugs or problems at this point in time."
        )


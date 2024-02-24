#
#example calling a view?
#https://semaphoreci.com/community/tutorials/getting-started-with-mocking-in-python

# Core Django imports
#from django.db import models
from django.test import Client
from django.test import TestCase
from django.urls import reverse

# Third-party app imports


# This project apps imports
from inventories.models import Ne
from inventories.models import OsCredential

from audits.libs import audits_ne

# Instantiate Client. Will use this instance throught all the tests.
client = Client()

context = {}
context['bodymessage'] = "Fake_FQDN" + ", Pigs in Space audit report"
from datetime import datetime
context['report_timestamp'] = datetime.now()
context['report_pass'] = [
    "PASS, Melody counts like a limp elephant",
    "PASS, Sebastian paints cockily",
    "PASS, Julie flies like a squirrel"
]
context['report_fail'] = [
    "FAIL, Pietro flies timidly",
    "FAIL, Sebastian runs supremely"
]
context['report_warning'] = [
    "WARNING, Pietro flies chancely"
]
context['ne_fqdn'] = "Fake_FQDN"
context['ne_id'] = "33"
context['audit_report'] = context['report_pass']
context['overall_audit_result'] = "PASS"
#print("This is the context dictionary in SetUp")
#print(context)

from unittest.mock import patch, Mock

class AuditViewsTests(TestCase):

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


    def tearDown(self):
        '''
        Clear fixtures for each individual test case.
        '''
        ## Log out
        #client.logout()
        pass

    from inventories.models import Ne
    from audits.views import ne_bogus
    @patch('audits.views.ne_bogus')
    def test_view_bogus(self, Mockne_bogus):
        blog = Mockne_bogus()
        blog.return_value = context
        #print(blog.return_value)
        pass


    def test_ne_bogus(self):
        ne1 = Ne.objects.get(fqdn = 'fqdn1')

        # I think this is what has to be faked somehow, the function: audits_ne.ne_audit_bogus(ne1.id)
        #context = audits_ne.ne_audit_bogus(ne1.id)
        #print("Next: direct call to raw function audits_ne.ne_audit_bogus")
        #print(context)

        response = client.get(
            reverse('audits:ne_bogus', args=(ne1.id,))
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'fqdn1, Pigs in Space audit r')

        #print("This is the context dictionary in the test itself")
        #print(context)

        #print("Next: response.data")
        #print(response.data)    # gives error -> AttributeError: 'HttpResponse' object has no attribute 'data'
        '''
        print("Next: response.content, which is a client get call to http://<>/audits/<ne.id>")
        print(response.content)

        print("Next: response.context['bodymessage']")
        print(response.context['bodymessage'])

        print("Next: response.client")
        print(response.client)

        print("Next: response.request")
        print(response.request)

        print("Next: response.status_code")
        print(response.status_code)

        print("Next: response.templates")
        print(response.templates)
        '''
        # mark

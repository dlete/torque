# Python standard libraries imports
from unittest.mock import patch
import socket

# Core Django imports
from django.test import TestCase

# Third-party app imports


# This project apps imports
from audits.libs import audits_ne
from inventories.models import Ne
from inventories.models import OsCredential


class AuditLibsAuditsNeGetMeNeAttributesTests(TestCase):
    '''
    Tests for the function get_me_ne_attributes
    '''

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
            #fqdn = 'fqdn1',
            fqdn = 'ntp1.heanet.ie',
            os_credential = osc1,
        )

        Ne.objects.create(
            fqdn = 'fqdn2',
            os_credential = osc1,
        )
        ne2 = Ne.objects.get(fqdn = 'fqdn2')

        Ne.objects.create(
            fqdn = 'fqdn3',
            os_credential = osc1,
        )
        ne3 = Ne.objects.get(fqdn = 'fqdn3')

        ne1 = Ne.objects.get(fqdn = 'ntp1.heanet.ie')
        ne1.nni_neighbors.add(ne2, ne3)


    def tearDown(self):
        '''
        Clear fixtures for each individual test case.
        '''
        ## Log out
        #client.logout()
        pass


    @patch('socket.gethostbyname', return_value='1.1.1.1')
    def test_ne_attributes(self, mock_socket_gethostbyname):
        ne1 = Ne.objects.get(fqdn = 'ntp1.heanet.ie')
        ne_attribs = audits_ne.get_me_ne_attributes(ne1.id)

        self.assertEqual(ne_attribs['username'], ne1.os_credential.username)
        self.assertEqual(ne_attribs['password'], ne1.os_credential.password)
        self.assertEqual(ne_attribs['nni_neighbors'], list(ne1.nni_neighbors.values_list('fqdn', flat=True)))
        self.assertEqual(mock_socket_gethostbyname.call_count, 1)
        self.assertEqual(ne_attribs['address_ipv4'], mock_socket_gethostbyname())


# Core Django imports
from django.test import TestCase
from django.db import IntegrityError

# This project apps imports
from .models import Ne
from .models import OsCredential


'''
In this file: Unittest for model Ne

TO DO
  DO NOT KNOW HOW TO PROVE THAT nni_neighbors CAN BE BLANK.
'''


class NeModelTests(TestCase):

    def setUp(self):
        '''
        Establish fixtures for each individual test case.
        '''
        OsCredential.objects.create(
            username="test_username1",
            password="test_password1",
        )
        osc1 = OsCredential.objects.get(username="test_username1")

        OsCredential.objects.create(
            username="test_username2",
            password="test_password2",
        )
        osc2 = OsCredential.objects.get(username="test_username2")

        Ne.objects.create(
            fqdn="ne1.acme.net",
            os_credential=osc1,
            #nni_neighbors="",
        )
        ne1 = Ne.objects.get(fqdn="ne1.acme.net")

        Ne.objects.create(
            fqdn="ne2.acme.net",
            os_credential=osc1,
            #nni_neighbors="",
        )
        ne2 = Ne.objects.get(fqdn="ne2.acme.net")

        ne = Ne(fqdn="ne.acme.net", os_credential=osc1)
        ne.save()
        ne.nni_neighbors.add(ne1, ne2)

    '''
    # If commented out
    # "An error occurred in the current transaction. You can't "
    # django.db.transaction.TransactionManagementError: An error occurred in 
    # the current transaction. 
    # You can't execute queries until the end of the 'atomic' block.
    def tearDown(self):
        #Clear fixtures for each individual test case.
        ne1 = Ne.objects.get(fqdn="ne1.acme.net")
        ne1.delete()
        ne2 = Ne.objects.get(fqdn="ne2.acme.net")
        ne2.delete()
        osc1 = OsCredential.objects.get(id=1)
        osc1.delete()
    '''
    
    def test_ne_create(self):
        '''
        Test Ne Create.

        Instanstiate an Ne object.
        Save the object to the database.
        Retrieve the object from the database.
        Verify the object sought was in the database.
        Verify the object is a Ne.
        Verify the object fields are the same than those that were saved.
        '''
        # Instanstiate an Ne object.
        #ne1 = Ne.objects.get(id=1)
        ne1 = Ne.objects.get(fqdn="ne1.acme.net")
        #ne2 = Ne.objects.get(id=2)
        ne2 = Ne.objects.get(fqdn="ne2.acme.net")
        #osc1 = OsCredential.objects.get(id=1)
        osc1 = OsCredential.objects.get(username="test_username1")
        ne = Ne(fqdn="test_ne_fqdn.acme.net", os_credential=osc1)
        # Instance needs to have a primary key value before a many-to-many 
        # relationship can be used
        #https://docs.djangoproject.com/en/1.11/topics/db/examples/many_to_many/
        ne.save()
        ne.nni_neighbors.add(ne1, ne2)

        # Save the object to the database.
        ne.save()
        #print(ne.nni_neighbors.all())
        #prints: <QuerySet [<Ne: ne1.acme.net>, <Ne: ne2.acme.net>]>

        # Retrieve the object from the database.
        ne = Ne.objects.get(fqdn="test_ne_fqdn.acme.net")

        # Verify the object sought was in the database.
        # Verify the object is a Ne.
        # Verify the object fields are the same than those that were saved.
        self.assertTrue(ne)
        self.assertIsInstance(ne, Ne)
        self.assertTrue(ne.fqdn == "test_ne_fqdn.acme.net")
        self.assertTrue(ne.os_credential==osc1)
        #https://stackoverflow.com/questions/11610943/django-1-4
        #-assertquerysetequal-how-to-use-method
        #https://docs.djangoproject.com/en/1.11/topics/testing/tools/
        self.assertQuerysetEqual(
            ne.nni_neighbors.all(), 
            [repr(r) for r in [ne1, ne2]]
        )


    def test_ne_read(self):
        '''
        Test Ne Read

        Retrieve object from the database.
        Verify object sought was in the database.
        Verify object fields are the same than those that were saved.
        '''
        ne = Ne.objects.get(fqdn="ne.acme.net")
        #ne1 = Ne.objects.get(id=1)
        ne1 = Ne.objects.get(fqdn="ne1.acme.net")
        #ne2 = Ne.objects.get(id=2)
        ne2 = Ne.objects.get(fqdn="ne2.acme.net")
        #osc1 = OsCredential.objects.get(id=1)
        osc1 = OsCredential.objects.get(username="test_username1")

        self.assertTrue(ne)
        self.assertEqual(ne.fqdn, "ne.acme.net")
        self.assertEqual(ne.os_credential, osc1)
        self.assertQuerysetEqual(
            ne.nni_neighbors.all(),
            [repr(r) for r in [ne1, ne2]]
        )


    def test_ne_update(self):
        '''
        Test Ne Update.
        
        Retrieve object from the database.
        Modify and then save the object.
        Retrieve modified object from the database.
        Verify object sought was in the database.
        Verify object fields are the same than those that were saved.
        Modify again the object to leave it as it was originally.
        '''
        #ne1 = Ne.objects.get(id=1)
        ne1 = Ne.objects.get(fqdn="ne1.acme.net")
        #ne2 = Ne.objects.get(id=2)
        ne2 = Ne.objects.get(fqdn="ne2.acme.net")
        #osc1 = OsCredential.objects.get(id=1)
        osc1 = OsCredential.objects.get(username="test_username1")
        #osc2 = OsCredential.objects.get(id=2)
        osc2 = OsCredential.objects.get(username="test_username2")
        ne = Ne.objects.get(fqdn="ne.acme.net")

        ''' Modify and then save the object. '''
        ne.fqdn = "updated_ne.acme.net"
        ne.os_credential=osc2
        ne.nni_neighbors.remove(ne2)
        ne.save()

        '''
        Retrieve modified object from the database.
        Verify object sought was in the database.
        Verify object fields are the same than those that were saved.
        '''
        ne = Ne.objects.get(fqdn="updated_ne.acme.net")
        self.assertTrue(ne)
        self.assertTrue(ne.fqdn == "updated_ne.acme.net")
        self.assertTrue(ne.os_credential==osc2)
        self.assertQuerysetEqual(
        ne.nni_neighbors.all(),
            [repr(r) for r in [ne1]]
        )

        '''
        Modify again the object to leave it as it was originally.
        Leave as it was so that tearDown can be executed.
        '''
        #ne.fqdn = "ne.acme.net"
        #ne.os_credential=osc1
        #ne.nni_neighbors.add(ne2)
        #ne.save()


    def test_ne_delete(self):
        '''
        Test Ne Delete.

        Create object.
        Delete object.
        Verify object has been deleted.
        '''
    
        ''' Create object.'''
        #ne1 = Ne.objects.get(id=1)
        ne1 = Ne.objects.get(fqdn="ne1.acme.net")
        #ne2 = Ne.objects.get(id=2)
        ne2 = Ne.objects.get(fqdn="ne2.acme.net")
        #osc1 = OsCredential.objects.get(id=1)
        osc1 = OsCredential.objects.get(username="test_username1")
        ne = Ne(fqdn="test_ne_fqdn.acme.net", os_credential=osc1)
        ne.save()
        #ne1 = Ne.objects.get(fqdn="ne1.acme.net")
        #ne2 = Ne.objects.get(fqdn="ne2.acme.net")
        ne.nni_neighbors.add(ne1, ne2)

        '''
        Delete ond verify object deletion.
        Verify object has been deleted.
        '''
        self.assertTrue(ne.delete())
        self.assertTrue(ne.id is None)


    def test_ne_method__str__(self):
        '''
        Test Ne Method __str__

        Retrieve object from the database.
        Verify that ouput of __str__() method is the same than object username.
        '''
        #ne = Ne.objects.get(id=1)
        ne = Ne.objects.get(fqdn="ne1.acme.net")
        self.assertEqual(ne.__str__(), ne.fqdn)


    def test_ne_unique_fqdn(self):
        '''
        Test Ne fqdn field is unique.

        Creating a Ne object with the same fqdn than an existing Ne
        (that is the username/password created in setUp) raises an
        IntegrityError exception.
        '''
        #osc1 = OsCredential.objects.get(id=1)
        osc1 = OsCredential.objects.get(username="test_username1")
        with self.assertRaises(IntegrityError):
            Ne.objects.create(
                fqdn="ne1.acme.net",
                os_credential=osc1,
            )


    def test_Ne_fqdn_max_lenght(self):
        '''
        Test Ne fqdn max_lenght.

        Retrieve object from the database.
        Verify that max_lenght object fields attribute is as defined in model.
        '''
        #ne = Ne.objects.get(id=1)
        ne = Ne.objects.get(fqdn="ne1.acme.net")
        max_length_fqdn = ne._meta.get_field('fqdn').max_length
        self.assertEqual(max_length_fqdn, 255)


    def test_Ne_fqdn_blank(self):
        '''
        Test Ne fqdn CANNOT be blank.

        Creating a Ne object with an empty fqdn field 
        raises an IntegrityError exception.
        '''
        with self.assertRaises(IntegrityError):
            Ne.objects.create(
                fqdn=None,
            )


    def test_ne_os_credential_blank(self):
        '''
        Test Ne os_credential CAN be blank.

        It is OK to create a Ne object with an empty os_credential field.
        Create Ne object with empty os_credential field.
        Retrieve Ne object from database.
        Verify the object sought was in the database.
        Verify the object is a Ne.
        Verify the object fields are the same than those that were saved.
        '''
        
        Ne.objects.create(
            fqdn="ne99.acme.net",
            os_credential=None,
        )
        ne = Ne.objects.get(fqdn="ne99.acme.net")
        
        self.assertTrue(ne)
        self.assertIsInstance(ne, Ne)
        #self.assertTrue(ne.fqdn == "ne99.acme.net")
        self.assertTrue(ne.os_credential == None),


    def test_ne_nni_neighbors_blank(self):
        '''
        Test Ne nni_neighbors CAN be blank.

        DO NOT KNOW HOW TO PROVE THAT nni_neighbors CAN BE BLANK.
        '''
        #osc1 = OsCredential.objects.get(id=1)
        osc1 = OsCredential.objects.get(username="test_username1")
        ne = Ne(fqdn="ne98.acme.net", os_credential=osc1)
        ne.save()

        self.assertTrue(ne)
        self.assertIsInstance(ne, Ne)


    def test_ne_on_delete_oscredential_foreignkey(self):
        '''
        Test Ne if we delete ForeignKey OsCredential, the Ne object
        is not deleted.

        Retrieve Ne object from the database.
        Delete the OsCredential object that is ForeignKey of Ne.
        Verify Ne object has not been deleted.
        Verify field OsCredential of object Ne has been set to Null.
        '''

        '''Retrieve Ne object from the database.'''
        ne = Ne.objects.get(fqdn="ne1.acme.net")
        #ne = Ne.objects.get(id=1)
        #osc1 = OsCredential.objects.get(id=1)
        osc1 = OsCredential.objects.get(username="test_username1")
        '''
        Verify the OsCredential field of the Ne object, so that when
        we delete that OsCredential object we are sure we are deleting
        the right OsCredential object.
        '''
        self.assertTrue(ne.os_credential==osc1)

        '''Delete the OsCredential object that is ForeignKey of Ne.'''
        osc1.delete()

        '''
        Verify Ne object has not been deleted.
        Verify the object sought was in the database.
        Verify the object is a Ne.
        Verify the object fields are the same than those that were saved.
        '''
        #ne = Ne.objects.get(id=1)
        ne = Ne.objects.get(fqdn="ne1.acme.net")
        self.assertTrue(ne)
        self.assertIsInstance(ne, Ne)
        '''
        Verify field OsCredential of object Ne has been set to Null.
        In Python, the 'null' object is the singleton None.
        https://stackoverflow.com/questions/3289601/null-object-in-python
        '''
        self.assertIs(ne.os_credential, None)

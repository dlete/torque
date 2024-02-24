# Core Django imports
from django.test import TestCase
from django.db import IntegrityError

# This project apps imports
from .models import OsCredential


'''
In this file: Unittest for model OsCredential
'''


class OsCredentialModelTests(TestCase):

    def setUp(self):
        '''
        Establish fixtures for each individual test case.
        '''
        OsCredential.objects.create(
            username="test_username1", 
            password="test_password1"
        )

    '''
    def tearDown(self):
        
        #To clean fixtures for each individual test case.
        
        osc_r = OsCredential.objects.get(username="test_username1")
        osc_r.delete()
    '''

    def test_OsCredential_create(self):
        '''
        Test OsCredential Create.

        Instanstiate and save an OsCredential object.
        Retrieve the object from the database.
        Verify the object sought was in the database.
        Verify the object is an OsCredential.
        Verify the object fields are the same than those that were saved.
        '''

        '''Instanstiate and save an OsCredential object.'''
        osc = OsCredential(username="test_username2", password="test_password2")
        osc.save()

        '''Retrieve the object from the database.'''
        osc = OsCredential.objects.get(username="test_username2")
        
        '''
        Verify the object sought was in the database.
        Verify the object is an OsCredential.
        Verify the object fields are the same than those that were saved.
        '''
        self.assertTrue(osc)
        self.assertIsInstance(osc, OsCredential)
        self.assertTrue(osc.username == "test_username2")
        self.assertTrue(osc.password == "test_password2")


    def test_OsCredential_read(self):
        '''
        Test OsCredential Read.

        Retrieve object from the database.
        Verify object sought was in the database.
        Verify object fields are the same than those that were saved.
        '''
        #osc = OsCredential.objects.get(id=1)
        osc = OsCredential.objects.get(username="test_username1")
        self.assertTrue(osc)
        self.assertTrue(osc.username == "test_username1")
        self.assertTrue(osc.password == "test_password1")


    def test_OsCredential_update(self):
        '''
        Test OsCredential Update.

        Retrieve object from database, modify and save back to database.
        Retrieve modified object from the database.
        Verify object sought was in the database.
        Verify object fields are the same than those that were saved.
        Modify again the object to leave it as it was originally.
        '''
        
        '''Retrieve object from database, modify and save back to database.'''
        #osc = OsCredential.objects.get(id=1)
        osc = OsCredential.objects.get(username="test_username1")
        osc.username = "test_username1_modified"
        osc.password = "test_password1_modified"
        osc.save()

        '''Retrieve modified object from the database.'''
        osc = OsCredential.objects.get(username="test_username1_modified")

        '''
        Verify object sought was in the database.
        Verify object fields are the same than those that were saved.
        '''
        self.assertTrue(osc)
        self.assertTrue(osc.username == "test_username1_modified")
        self.assertTrue(osc.password == "test_password1_modified")

        ''' 
        Modify again the object to leave it as it was originally.
        Leave as it was so that tearDown can be executed.
        '''
        osc.username = "test_username1"
        osc.password = "test_password1"
        osc.save()


    def test_OsCredential_delete(self):
        '''
        Test OsCredential Delete.

        Retrieve object from the database.
        Delete object.
        Verify object has been deleted.
        '''

        #osc = OsCredential.objects.get(id=1)
        osc = OsCredential.objects.get(username="test_username1")
        self.assertTrue(osc.delete())
        ''' 
        If you try to delete a non-existing object you would get:

        AssertionError: OsCredential object can't be deleted because its id 
        attribute is set to None.

        Use the above to prove that the object has been in fact deleted.
        '''
        self.assertTrue(osc.id is None)


    def test_OsCredential_method__str__(self):
        '''
        Test OsCredential Method __str__

        Retrieve object from the database.
        Verify that ouput of __str__() method is the same than object username.
        '''
        #osc = OsCredential.objects.get(id=1)
        osc = OsCredential.objects.get(username="test_username1")
        self.assertEqual(osc.__str__(), osc.username)


    def test_OsCredential_unique_username(self):
        '''
        Test OsCredential username field is unique

        Creating an OsCredential object with the same username than an existing
        one (that is the username/password created in setUp) raises an 
        IntegrityError exception.
        '''
        with self.assertRaises(IntegrityError):
            OsCredential.objects.create(
                username="test_username1",
                password="test_password1"
            )


    def test_OsCredential_max_lenght(self):
        '''
        Test OsCredential username and password max_lenght

        Retrieve object from the database.
        Verify that max_lenght object fields attribute is as defined in model.
        '''
        osc = OsCredential.objects.get(username="test_username1")
        max_length_username = osc._meta.get_field('username').max_length
        max_length_password = osc._meta.get_field('password').max_length
        self.assertEqual(max_length_username,64)
        self.assertEqual(max_length_password,64)


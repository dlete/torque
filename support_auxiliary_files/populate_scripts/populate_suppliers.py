''' 
    TO USE:
        Move file to the root of the Django project. That is the directory
        where the manage.py file lives.
    Description:
        Populates the Supplier model of the catalogues app. Runs through the 
        lines of a csv file with a pair of supplier name/abbreviation entries
        in each of them. Creates a Supplier object and saves it to database.
    Input:
        CSV file with list of Supplier to add.
    Output:
        Adds Supplier objects to the Supplier model in the catalogues app.
    Requires:
        Be in the Django environment/console. Be in the equivalent to:
        python manage.py startshell
    Credits:
        Code based on http://www.tangowithdjango.com/book17/chapters/models.html
'''
# set the Python environment to use Django. Equivalent to "python manage.py startshell"
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'torque.settings')
import django
django.setup()
from catalogues.models import Supplier


def add_supplier(name, abbreviation):
    '''
    Description:
        Generic function to add a Supplier object to the database.
	Input: 
		name (str) representing the name field of the Supplier object.
        abbreviation (str) representing the abbreviation field of the 
            Supplier object.
	Output:
        One (1) Supplier object.
		The Supplier will have been added to the Supplier model of the 
        catalogues app.
    '''
    # The trick with the get_or_create method is that it actually returns a 
    # tuple of (object, created). The first element is an instance of the 
    # model you are trying to retrieve and the second is a boolean flag to 
    # tell if the instance was created or not. True means the instance was 
    # created by the get_or_create method and False means it was retrieved 
    # from the database.
    s = Supplier.objects.get_or_create(name=name, abbreviation=abbreviation)[0]
    #s.save()
    return s


def populate():
    '''
    Description
        Invokes as many times as you want the generic function to add Supplier
        objects to the database.
    '''
    import csv
    with open('core/cli_not_in_use_anymore/libs/scraps/heanet_suppliers.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            if bool(row['name']):
                name = row['name']
                abbreviation = row['abbreviation']
                add_supplier(name, abbreviation)
            else:
                break

        # Print out what we have added to the user.
        for s in Supplier.objects.all():
            print(s)


# Start execution here!
if __name__ == '__main__':
    print("Starting Supplier population script...")
    populate()

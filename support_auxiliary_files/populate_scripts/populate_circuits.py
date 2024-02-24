'''
    TO USE:
        Move file to the root of the Django project. That is the directory
        where the manage.py file lives.
    Description:
        Populates the Circuit model of the inventory app. Runs through the 
        lines of a csv file with all the necessary fields to create a circuit
        in each of the rows. Creates a Circuit object and saves it to database.
    Input:
        CSV file with list of Circuits to add.
    Output:
        Adds Circuit objects to the Circuit model in the inventory app.
    Requires:
        Be in the Django environment/console. Be in the equivalent to:
        python manage.py startshell
    Credits:
        Code based on http://www.tangowithdjango.com/book17/chapters/models.html
'''

# set the Python environment to use Django. 
# Equivalent to "python manage.py startshell"
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'torque.settings')
import django
django.setup()
from catalogues.models import Supplier
from inventories.models import Circuit


def add_circuit(supplier, circuit_id, a_end, b_end, ctype, cinfo):
    '''
    Description:
        Generic function to add a Circuit object to the database.
	Input: 
		name (str) representing the name field of the Supplier object.
        abbreviation (str) representing the abbreviation field of the 
            Supplier object.
	Output:
        One (1) Supplier object.
		The Supplier will have been added to the Supplier model of the 
        catalogues app.
    '''
    supplier = Supplier.objects.get(id=supplier)
    c = Circuit.objects.get_or_create(
        supplier = supplier, 
        circuit_id = circuit_id,
        a_end_description = a_end,
        b_end_description = b_end,
        circuit_type = ctype,
        circuit_info = cinfo
    )[0]
    #c.save()
    return c


def populate():
    '''
    Description
        Invokes as many times as you want the generic function to add Circuit
        objects to the database.
    '''
    import csv
    import codecs
    #with open('core/cli/libs/scraps/heanet_circuits.csv', 'r') as csvfile:
    #with codecs.open('core/cli/libs/scraps/heanet_circuits.csv', 'r', encoding='utf-8') as csvfile:
    #with open('core/cli/libs/scraps/heanet_circuits.csv', 'r', encoding='iso-8859-1') as csvfile:
    #cli_not_in_use_anymore
    with open('core/cli_not_in_use_anymore/libs/scraps/heanet_circuits.csv', 'r', encoding='iso-8859-1') as csvfile:
    #with open('core/cli/libs/scraps/heanet_suppliers.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            print(row)
            if bool(row['supplier']):
                #this has to be a query
                s = Supplier.objects.get(abbreviation=row['supplier'])
                print(s)
                supplier = s.id
                print(supplier)
                circuit_id = row['circuit_id']
                a_end_description = row['a_end']
                b_end_description = row['b_end']
                circuit_type = row['ctype']
                circuit_info = row['cinfo']

                add_circuit(supplier, circuit_id, a_end_description, b_end_description, circuit_type, circuit_info)
            else:
                break

        # Print out what we have added to the user.
        for i in Circuit.objects.all():
            print(i)


# Start execution here!
if __name__ == '__main__':
    print("Starting Circuit population script...")
    populate()

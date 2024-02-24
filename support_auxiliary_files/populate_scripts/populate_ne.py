'''
    TO USE:
        Move file to the root of the Django project. That is the directory
        where the manage.py file lives.
    Description:
        Populates the Ne model of the inventory app. Runs through a list of FQDN,
        creates a Ne object and saves it to database.
    Input:
        CSV file with list of FQDN to add. FQDN is in the first position of each row.
    Output:
        Adds Ne objects to the Ne model in the inventory app.
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
from inventory.models import Ne
from inventory.models import OsCredential


def add_ne(fqdn):
    '''
    Description:
        Generic function to add an Ne object to the database.
	Input: 
		One (1) string representing a FQDN.
	Output:
        One (1) Ne object.
		The Ne will have been added to the Ne model of the inventory app.
    '''
    n = Ne.objects.get_or_create(fqdn=fqdn)[0]
    os_credential = OsCredential.objects.get(username='rancid')
    n.os_credential=os_credential
    n.save()
    return n


def populate():
    '''
    Description
        Invokes as many times as you want the generic function to add Ne
        objects to the database
    '''
    #os_credential = OsCredential.objects.get(username='rancid')

    #add_ne(
    #    fqdn="testdevice_fqdn")

    OsCredential.objects.create(
        username = 'rancid',
        password = '#pW5MV4G!q%3341sfsdFSS!@',
    )



    import csv
    my_domain = ".nn.hea.net"
    with open('core/cli/libs/scraps/rman_model_hostname.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            # In case there are empty values in the CSV
            # # https://stackoverflow.com/questions/12319950/how-do-i-identify-the-blank-fields-in-the-csv-file-in-python
            if bool(row['FQDN']):
                fqdn = row['FQDN'] + my_domain
                #print("FQDN is: " + row['FQDN'] + my_domain)
                print("FQDN is: " + fqdn)
                add_ne(fqdn=fqdn)

                if row['NNI1'] != "empty":
                    print("NNI #1 is: " + row['NNI1'] + my_domain)
                else:
   	                print("NNI #1 is: empty")

                if row['NNI2'] != "empty":
                	print("NNI #2 is: " + row['NNI2'] + my_domain)
                else:
                    print("NNI #2 is: empty")

                if row['NNI3'] != "empty":
                	print("NNI #3 is: " + row['NNI3'] + my_domain)
                else:
                	print("NNI #3 is: empty")

                if row['NNI4'] != "empty":
                	print("NNI #4 is: " + row['NNI4'] + my_domain)
                else:
                	print("NNI #4 is: empty")
            else:
                break



    # Print out what we have added to the user.
    for c in Ne.objects.all():
        print(c)


# Start execution here!
if __name__ == '__main__':
    print("Starting Ne population script...")
    populate()

'''
    TO USE:
        Move file to the root of the Django project. That is the directory
        where the manage.py file lives.
    Description:
        Populates the nni_neighbors in Ne model of the inventory app. Runs through a list 
        of FQDN and NNI relations, retrieves the Ne from the database and adds the 
        nni_neighbors in the file.
    Input:
        CSV file with list of FQDN and NNI neighbors to add. 
        FQDN is in the first position of each row.
        NNI neighbors are in subsequent positions.
    Output:
        Adds nni_neighbors to an existing Ne object.
    Requires:
        Be in the Django environment/console. Be in the equivalent to:
        python manage.py startshell
    Credits:
        Code based on http://www.tangowithdjango.com/book17/chapters/models.html

https://docs.djangoproject.com/en/1.11/topics/db/examples/many_to_many/
python manage.py shell
from inventory.models import Ne
ne1 = Ne.objects.get(fqdn='edge1-dcu-glasnevin.nn.hea.net')
ne2 = Ne.objects.get(fqdn='edge1-dcu-spd.nn.hea.net')
nni1 = Ne.objects.get(fqdn='edge1-dcu.nn.hea.net')
nni2 = Ne.objects.get(fqdn='edge2-dcu.nn.hea.net')
ne1.nni_neighbors.add(nni1)
ne1.nni_neighbors.add(nni2)
'''
# set the Python environment to use Django. Equivalent to "python manage.py startshell"
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'torque.settings')
import django
django.setup()
from inventory.models import Ne
from inventory.models import OsCredential


def add_nni_neighbor(fqdn_ne, fqdn_nni_neighbor):
    '''
    Description:
        Generic function to add a nni_neighbor to a Ne object.
	Input: 
		One (1) string representing the FQDN of the Ne. 
        One (1) string representing the FQDN of the nni_neighbor.
	Output:
        #One (1) Ne object.
		The Ne will have been added one (1) nni_neighbor.
    '''
    ne = Ne.objects.get_or_create(fqdn=fqdn_ne)[0]
    nni = Ne.objects.get_or_create(fqdn=fqdn_nni_neighbor)[0]
    print("This is the Ne: " + ne.fqdn)
    print("This is the nni_neighbor that I will add: " + nni.fqdn)
    ne.nni_neighbors.add(nni)
    #n.save()
    return ne

def populate():
    '''
    Description
        Invokes as many times as you want the generic function to add
        nni_neighbors object to the database.
    '''

    #add_ne(
    #    fqdn="testdevice_fqdn")


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
                #print("FQDN is: " + fqdn)

                if row['NNI1'] != "empty":
                    #print("NNI #1 is: " + row['NNI1'] + my_domain)
                    fqdn_nni_neighbor = row['NNI1'] + my_domain
                    add_nni_neighbor(fqdn_ne=fqdn, fqdn_nni_neighbor=fqdn_nni_neighbor)
                else:
                    #print("NNI #1 is: empty")
                    add_nni_neighbor(fqdn_ne=fqdn, fqdn_nni_neighbor=fqdn)
                    #pass

                if row['NNI2'] != "empty":
                    #print("NNI #2 is: " + row['NNI2'] + my_domain)
                    fqdn_nni_neighbor = row['NNI2'] + my_domain
                    add_nni_neighbor(fqdn_ne=fqdn, fqdn_nni_neighbor=fqdn_nni_neighbor)
                else:
                    #print("NNI #2 is: empty")
                    pass

                if row['NNI3'] != "empty":
                    #print("NNI #3 is: " + row['NNI3'] + my_domain)
                    fqdn_nni_neighbor = row['NNI3'] + my_domain
                    add_nni_neighbor(fqdn_ne=fqdn, fqdn_nni_neighbor=fqdn_nni_neighbor)
                else:
                    #print("NNI #3 is: empty")
                    pass

                if row['NNI4'] != "empty":
                    #print("NNI #4 is: " + row['NNI4'] + my_domain)
                    fqdn_nni_neighbor = row['NNI4'] + my_domain
                    add_nni_neighbor(fqdn_ne=fqdn, fqdn_nni_neighbor=fqdn_nni_neighbor)
                else:
                    #print("NNI #4 is: empty")
                    pass
            else:
                break



    # Print out what we have added to the user.
    #for c in Ne.objects.all():
    #    print(c)


# Start execution here!
if __name__ == '__main__':
    print("Starting Ne population script...")
    populate()

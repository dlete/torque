import csv

my_domain = ".nn.hea.net"
with open('rman_model_hostname.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for row in reader:
        # In case there are empty values in the CSV
        # https://stackoverflow.com/questions/12319950/how-do-i-identify-the-blank-fields-in-the-csv-file-in-python
        if bool(row['FQDN']):
            #print(row)
            print("FQDN is: " + row['FQDN'] + my_domain)

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

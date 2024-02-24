import csv

with open('rman_model.csv', 'r') as f:
    reader = csv.reader(f, delimiter=';')
    your_list = list(reader)

#print(your_list)
for line in your_list:
    #print(line)
    print("FQDN is: " + line[0])
    print("NNI #1 is: " + line[1])
    print("NNI #2 is: " + line[2])
    print("NNI #3 is: " + line[3])
    print("NNI #4 is: " + line[4])

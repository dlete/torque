
def audit_jnpr_nni_desc(address_ip, os_username, os_password):
    '''Return list of test results for NNI description.

    Args:
        address_ip (str)
        os_username (str)
        os_password (str)

    Returns:
        list: each item in the list is a line of text. Each line of text begins$
        with either of the keywords: PASS, FAIL, or WARNING. These first$
        keywords are always in capital letters.

    Requires:
        Python 3.5.2
        junos-eznc 2.1.3

    To-do:
        If PASS, add what circuit_id it is being matched.
    '''


    ''' Initialize, empty, the list that the function will return. '''
    list_report = []

    # Get ALL the circuit id from the authoritative repository.
    # At the moment in a database, in the future we should be able to
    # get that list through an API call.
    import MySQLdb
    db = MySQLdb.connect("localhost", "torque", "Friday13", "torque")
    cursor = db.cursor()
    #query = ("SELECT * FROM inventory_circuit")
    query = ("SELECT * FROM inventories_circuit")
    cursor.execute(query)
    results = cursor.fetchall()
    list_circuit_ids = []
    for row in results:
        #print(row)
        #print(row[1])
        list_circuit_ids.append(row[1])
    #for i in list_circuit_ids:
    #    print(i)
    db.close()
    # Now we have ALL the circuit ID from the authoritative repository
    # in the list list_circuit_ids

    #'''MOCK UP START'''
    ## list of descriptions, bogus
    #list_if_descriptions = []
    #if_descrip = 'ip_transit_201707210944'
    #list_if_descriptions.append(if_descrip)
    #if_descrip = 'educampus_201707210944'
    #list_if_descriptions.append(if_descrip)
    #if_descrip = 'edge1-dcu xe-0/0/1, WES586110997'
    #list_if_descriptions.append(if_descrip)

    #print("FIRST PASS")
    #for d in list_if_descriptions:
    #    print(d)
    #    for i in list_circuit_ids:
    #        #print(i)
    #        if i in d:
    #            #list_report.append("PASS, ")
    #            if_nni_description_audit = "PASS, NNI interface p.key description: " + d + " does contain circuit id " + i
    #            break
    #        else:
    #            if_nni_description_audit = "FAIL, "
    #            #list_report.append("FAIL, ")
    #    list_report.append(if_nni_description_audit)

    #print("SECOND PASS")
    #for d in list_if_descriptions:
    #    print(d)
    #    l = d.split(' ')
    #    print(l)
    #    print(type(l))
    #    #cross = set(list_circuit_ids).intersection(list_if_descriptions)
    #    cross = set(list_circuit_ids).intersection(l)
    #    print("THIS IS cross")
    #    print(cross)
    #    print("TYPE FOR cross IS")
    #    print(type(cross))
    #    print(len(cross))
    #    print(type(len(cross)))
    #    if len(cross) > 0:
    #        list_report.append("PASS, NNI interface p.key description: " + d + " does contain circuit id " + i)
    #    else:
    #        list_report.append("FAIL, NNI interface p.key description: " + d + " does not contain a circuit id")
    #'''MOCK UP END'''

    # THIS WORKS!!!!
    ''' Import junos-eznc base function and open Netconf session. '''
    from jnpr.junos import Device
    try:
        Device.auto_probe = 5
        device = Device(host=address_ip, user=os_username, password=os_password, gather_facts=False)
        device.open()
    except Exception as err:
        list_report.append("WARNING, the following error has happened: " + str(err))
        return list_report

    ''' Retrieve information. '''
    from jnpr.junos.op.phyport import PhyPortTable
    phyPorts = PhyPortTable(device).get()


    # TEST, if it is a NN port it must have a circuit ID in the description
    for p in phyPorts:
        if (p.description is not None) and ('NN' in p.description):
            # convert interface description to a list
            l = p.description.split(' ')
            cross = set(list_circuit_ids).intersection(l)
            # len(cross) is of type int
            if len(cross) > 0:
                list_report.append("PASS, NNI interface " + p.key + 
                    " description: " + p.description + 
                    " does contain a circuit id.")
            else:
                list_report.append("FAIL, NNI interface " + p.key + 
                    " description: " + p.description + 
                    " does not contain a circuit id.")

    #print("there are this many elements in the list")
    #print(len(list_report))
    # TEST, there is at least one (1) NNI interface configured.
    if len(list_report) == 0:
        list_report.append("FAIL, there are no NNI interfaces configured.")
    else:
        list_report.append("PASS, there is at least one (1) NNI interface configured.")

    return list_report

'''
# mark
####  CONSTANTS  ####
fqdn = 'edge3-testlab.nn.hea.net'
nni_neighbors_expected = [ 'edge1-testlab', 'edge88-testlab' ]
local_username = 'heanet'
local_password = 'KqV7X98v!'

#fqdn = 'edge1-qqi-denzille.nn.hea.net'
#fqdn = 'edge1-qqi-mount.nn.hea.net'
fqdn = 'dist1-lyit1.nn.hea.net'
#fqdn = 'dist1-lyit2.nn.hea.net'
local_username = 'rancid'
local_password = '#pW5MV4G!q%3341sfsdFSS!@'
####  CONSTANTS  ####

import socket
address_ipv4 = (socket.gethostbyname(fqdn))
#address_ipv6 = socket.getaddrinfo(fqdn, None, socket.AF_INET6)[0][4][0]

#address_ipv4 = '193.2.2.2'
phyport_audit_report = audit_jnpr_nni_desc(address_ipv4, local_username, local_password)
for i in phyport_audit_report:
    print(i)
'''

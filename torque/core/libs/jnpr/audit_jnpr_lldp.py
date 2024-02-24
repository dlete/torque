
def audit_jnpr_lldp(address_ipv4, os_username, os_password, lldp_neighbors_expected):
    '''Return list of test results for an LLDP neighbors.

    Args:
        address_ip (str)
        os_username (str)
        os_password (str)
        peers_expected (list)

    Returns:
        list: each item in the list is a line of text. Each line of text begins
        with either of the keywords: PASS, FAIL, or WARNING. These first
        keywords are always in capital letters.

    Requires:
        Python 3.5.2
        junos-eznc 2.1.3

    To-do:
        Add error handling. We are not checking what to do if we can't connect
        to the Device.
    '''

    ''' Initialize, empty, the list that the function will return. '''
    list_report = []

    ''' Import junos-eznc base function and open Netconf session. '''
    from jnpr.junos import Device
    try:
        Device.auto_probe = 5 
        device = Device(
            host=address_ipv4,
            user=os_username,
            password=os_password,
            gather_facts=False)
        device.open()
    except Exception as err:
        list_report.append("WARNING, the following error has happened: " + str(err))
        return list_report
    

    ''' Retrieve information. '''
    from jnpr.junos.op.lldp import LLDPNeighborTable
    neighbors_seen = LLDPNeighborTable(device).get()

    ##print(device.facts)
    #'''
    #This is a little hack. In this network, MX480, MX960 and ACX5048 have
    #two links between them (MX to ACX that is). The database model in 
    #Django does not reflect more than one link. Hence we have to add one (1)  
    #more neighbor from the onset in this script to the NUMBER of expected
    #LLDP neighbors.
    #'''
    #model = device.facts['model']
    #if (model == 'MX480' or model == 'MX960'):
    #    number_of_neighbors_expected = len(lldp_neighbors_expected) + 1
    #elif model is None:
    #    if "ACX5K" in device.facts['RE0']['model']:
    #        if any('core' in s for s in lldp_neighbors_expected):
    #            # https://stackoverflow.com/questions/4843158/check-if-a-python-list-item-contains-a-string-inside-another-string
    #            # if we are auditing an ACX5K and any of the neighbors is 
    #            # a core router, e.g. has the form core[1|2]-[xxxx], then we
    #            # are connected with 2 x 10G, hence we will see that neighbor
    #            # twice => add 1 to the number of expected neighbors.
    #            number_of_neighbors_expected = len(lldp_neighbors_expected) + 1
    #        #if 'core' not in lldp_neighbors_expected:
    #        else:
    #            number_of_neighbors_expected = len(lldp_neighbors_expected)
    #
    #else:
    #    number_of_neighbors_expected = len(lldp_neighbors_expected)

    ''' Find out what type of chassis we are dealing with '''
    from lxml import etree
    chassis_inventory = device.rpc.get_chassis_inventory()
    for element in chassis_inventory.findall('.//chassis'):
        chassis_description = element.find('description').text

    '''
    This is a little hack. In this network, MX480, MX960 and ACX5048 have
    two links between them (MX to ACX that is). The database model in
    Django does not reflect more than one link. Hence we have to add one (1)
    more neighbor from the onset in this script to the NUMBER of expected
    LLDP neighbors.
    '''
    if (chassis_description == 'MX960' or chassis_description == 'MX480'):
        number_of_neighbors_expected = len(lldp_neighbors_expected) + 1
    elif (chassis_description == 'ACX5048'):
        if any('core' in s for s in lldp_neighbors_expected):
            '''
            https://stackoverflow.com/questions/4843158/check-if-a-python-list-item-contains-a-string-inside-another-string
            if we are auditing an ACX5K and any of the neighbors is
            a core router, e.g. has the form core[1|2]-[xxxx], then we
            are connected with 2 x 10G, hence we will see that neighbor
            twice => add 1 to the number of expected neighbors.
            '''
            number_of_neighbors_expected = len(lldp_neighbors_expected) + 1
        else:
            number_of_neighbors_expected = len(lldp_neighbors_expected)
    else:
        number_of_neighbors_expected = len(lldp_neighbors_expected)


    number_of_neighbors_seen = neighbors_seen.__len__()


    # TEST, the NUMBER of LLDP neighbors EXPECTED and SEEN is the SAME
    if number_of_neighbors_seen == number_of_neighbors_expected:
        #list_report.append("PASS, the number of LLDP neighbors seen and expected is the same.")
        list_report.append("PASS, the expected number of LLDP neighbors is " + 
            str(number_of_neighbors_expected) + " and you are seeing " +
            str(number_of_neighbors_seen) + " LLDP neighbors."
        )
    else:
        #list_report.append("FAIL, the NUMBER of LLDP neighbors seen and expected is NOT the same.")
        list_report.append("FAIL, the expected number of LLDP neighbors is " +
            str(number_of_neighbors_expected) + " and you are seeing " +
            str(number_of_neighbors_seen) + " LLDP neighbors."
        )


    ''' Build a list with the hostnames of the LLDP neighbors we are seeing'''
    list_neighbors_seen = []
    for neighbor_seen in neighbors_seen:
        list_neighbors_seen.append(neighbor_seen.remote_sysname)
    neighbors_expected = lldp_neighbors_expected

    # TEST, What you expected to see, you see
    for neighbor_expected in neighbors_expected:
        #print("neighbor_expected")
        #print(neighbor_expected)
        if neighbor_expected in list_neighbors_seen:
            list_report.append("PASS, you expected to see LLDP neighbor " +
                neighbor_expected + " and you are seeing " +
                neighbor_expected + "."
            )
        else:
            list_report.append("FAIL, you expected to see LLDP neighbor " +
                neighbor_expected + " but is not seen."
            )


    # TEST, What you see, was expected
    for neighbor_seen in neighbors_seen:
        if neighbor_seen.remote_sysname in neighbors_expected:
            list_report.append("PASS, you see LLDP neighbor " +
                neighbor_seen.remote_sysname +
                " and that was expected."
            )
        else:
            list_report.append("FAIL, you see LLDP neighbor " +
                neighbor_seen.remote_sysname +
                " and that was NOT expected."
            )


    device.close()
    return list_report

'''
# mark
# To test this function, uncomment this block
####  CONSTANTS  ####
#fqdn = 'edge1-testlab.nn.hea.net'
#fqdn = 'edge2-testlab.nn.hea.net'
fqdn = 'edge3-testlab.nn.hea.net'
nni_neighbors_expected = [ 'edge1-testlab', 'edge88-testlab' ]
local_username = 'heanet'
local_password = 'KqV7X98v!'

#fqdn = 'edge4-testlab.nn.hea.net'
#fqdn = 'edge5-testlab.nn.hea.net'
#local_username = 'heanet'
#local_password = '$!3u$uxqDMTXzw9'

#fqdn = 'edge1-dcu-glasnevin.nn.hea.net'
#fqdn = 'edge1-dcu-spd2.nn.hea.net'
#nni_neighbors_expected = ['edge1-dcu-spd1', 'edge2-dcu']
#fqdn = 'edge1-dcu.nn.hea.net'
#nni_neighbors_expected = ['core1-dcu', 'edge1-dcu-glasnevin', 'edge1-dcu-spd1']
#fqdn = 'dist1-lyit2.nn.hea.net'
#fqdn = 'rr1-pw.nn.hea.net'
#fqdn = 'core2-blanch.nn.hea.net'
#fqdn = 'core2-pw.nn.hea.net'
#local_username = 'rancid'
#local_password = '#pW5MV4G!q%3341sfsdFSS!@'
####  CONSTANTS  ####

import socket

try:
    address_ip = (socket.gethostbyname(fqdn))
except Exception as err:
    print(str(err))

audit_report = audit_jnpr_lldp(address_ip, local_username, local_password, nni_neighbors_expected)
for i in audit_report:
    print(i)
'''

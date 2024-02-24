
def audit_juniper_lldp(address_ipv4, os_username, os_password, lldp_neighbors_expected):
    # initialize an empty list, this is what the function will return
    list_report = []

    from jnpr.junos import Device
    device = Device(host=address_ipv4, user=os_username, password=os_password)
    device.open(gather_facts=False)

    from jnpr.junos.op.lldp import LLDPNeighborTable
    neighbors_seen = LLDPNeighborTable(device).get()
    '''
    list_neighbors_seen = []
    for neighbor_seen in neighbors_seen:
        list_neighbors_seen.append(neighbor_seen.remote_sysname)
    '''
    number_of_neighbors_expected = len(lldp_neighbors_expected)
    number_of_neighbors_seen = neighbors_seen.__len__()

    # TEST, the NUMBER of LLDP neighbors EXPECTED and SEEN is the SAME
    if number_of_neighbors_seen == number_of_neighbors_expected:
        list_report.append("PASS, the number of LLDP neighbors seen and expected is the same.")
    else:
        list_report.append("FAIL, the NUMBER of LLDP neighbors seen and expected is NOT the same.")


    list_neighbors_seen = []
    for neighbor_seen in neighbors_seen:
        list_neighbors_seen.append(neighbor_seen.remote_sysname)
    neighbors_expected = lldp_neighbors_expected


    # TEST, What you expected to see, you see
    for neighbor_expected in neighbors_expected:
        if neighbor_expected in list_neighbors_seen:
            list_report.append("PASS, you expected to see " + neighbor_expected + " and you are seeing " + neighbor_seen.remote_sysname)
        else:
            list_report.append("FAIL, you expected to see " + neighbor_expected + " and you do not see it.")


    # TEST, What you see, was expected
    for neighbor_seen in neighbors_seen:
        if neighbor_seen.remote_sysname in neighbors_expected:
            list_report.append("PASS, you see " + neighbor_seen.remote_sysname + " and that was expected.")
        else:
            list_report.append("FAIL, you see " + neighbor_seen.remote_sysname + " and that was NOT expected. " )


    device.close()
    return list_report



# To test this function, uncomment this block
####  CONSTANTS  ####
fqdn = 'edge3-testlab.nn.hea.net'
nni_neighbors_expected = [ 'edge1-testlab', 'edge88-testlab' ]
print(nni_neighbors_expected)
local_username = 'heanet'
local_password = 'KqV7X98v!'
####  CONSTANTS  ####

import sys
import socket
try:
    address_ip = (socket.gethostbyname(fqdn))
except:
    exit(0)
    e = sys.exc_info()[0]
    print(e)


report_juniper_lldp = audit_juniper_lldp(address_ip, local_username, local_password, nni_neighbors_expected)
for l in report_juniper_lldp:
    print(l)


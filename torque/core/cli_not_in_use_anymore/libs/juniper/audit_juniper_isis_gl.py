def audit_juniper_isis(address_ipv4, os_username, os_password, isis_parameters, isis_database):
    # initialize an empty list, this is what the function will return
    list_report = []

    from jnpr.junos import Device
    device = Device(host=address_ipv4, user=os_username, password=os_password)
    device.open(gather_facts=False)

    from jnpr.junos.op.isis import IsisAdjacencyTable
    isis_table = IsisAdjacencyTable(device).get()
    
    from lxml import etree 

    for isis_parameters in isis_table:
#        print(isis_parameters.level)
#        print(isis_parameters.circuit_type)
        
        if isis_parameters.level != isis_level:
           list_report.append("ISIS LEVEL FAIL, EXPECTED ISIS LEVEL: " + isis_level + ", " + "ACTUAL ISIS LEVEL: " + isis_parameters.level)
        else:
            list_report.append("ISIS LEVEL PASS, EXPECTED ISIS LEVEL: " + isis_level + ", " + "ACTUAL ISIS LEVEL: " + isis_parameters.level)
        
        if isis_parameters.circuit_type != isis_circuit_type:
            list_report.append("ISIS CIRCUIT TYPE FAIL, EXPECTED ISIS CIRCUIT TYPE " + isis_circuit_type + ", " + "ACTUAL ISIS CIRCUIT TYPE: " + isis_parameters.circuit_type)
        else:
            list_report.append("ISIS CIRCUIT TYPE PASS, EXPECTED ISIS CIRCUIT TYPE: " + isis_level + ", " + "ACTUAL ISIS CIRCUIT TYPE: " + isis_parameters.level)

#        print(isis_parameters.system_name)  

#    lsp_count = []
    isis_database = device.rpc.get_isis_database_information({'format': 'json'})
 
    lsp_count_l1=isis_database['isis-database-information'][0]['isis-database'][0]['lsp-count'][0]['data']
#    print(lsp_count_l1)

    if lsp_count_l1 != '0':
        list_report.append("L1 LSP CHECK FAIL, L1 LSPs in L1 LSDB")
    else:
        list_report.append("L1 LSP CHECK PASS, NO L1 LSPs in L1 LSDB")

    from pprint import pprint
    pprint(isis_database)

#    etree.dump(isis_database)

#    print(isis_database.findtext("isis-database/lsp-count"))

    device.close()
    return list_report

# To test this function, uncomment this block
####  CONSTANTS  ####
fqdn = 'edge3-testlab.nn.hea.net'
#nni_neighbors_expected = [ 'edge1-testlab', 'edge88-testlab' ]
#print(nni_neighbors_expected)
isis_level = '2'
isis_circuit_type = '2'
isis_neighbors_expected = 'edge1-testlab'
lsp_count_l1 = '0'
#lsp_count_l2 = []
isis_parameters = isis_level, isis_circuit_type, lsp_count_l1 
isis_database = []
local_username = 'heanet'
local_password = 'KqV7X98v!'
####  CONSTANTS  ####
import os 
import sys
import socket

try:
    address_ip = (socket.gethostbyname(fqdn))
except:
    exit(0)
    e = sys.exc_info()[0]
    print(e)

report_juniper_isis = audit_juniper_isis(address_ip, local_username, local_password, isis_parameters, isis_database)
for l in report_juniper_isis:
    print(l)


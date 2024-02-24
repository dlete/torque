from audit_juniper_lldp import audit_juniper_lldp
#from audit_juniper_bgp import audit_jnpr_ibgp
#from audit_jnpr_phyport import audit_jnpr_phyport
#from audit_juniper_pic import audit_transceivers_juniper
#from audit_jnpr_os import audit_jnpr_os

def audit_jnpr_ne_one(address_ipv4, os_username, os_password, nni_neighbors_expected):
    list_report = []
    ibgp_peers_expected = ['87.44.48.5', '87.44.48.6', '2001:770:200::5', '2001:770:200::6']

    #report_jnpr_os = audit_jnpr_os(address_ipv4, os_username, os_password)
    #list_report = list_report + report_jnpr_os

    #report_jnpr_pic = audit_transceivers_juniper(address_ipv4, os_username, os_password)
    #list_report = list_report + report_jnpr_pic

    #report_jnpr_phyport = audit_jnpr_phyport(address_ipv4, os_username, os_password)
    #list_report = list_report + report_jnpr_phyport

    report_jnpr_lldp = audit_juniper_lldp(address_ip, os_username, os_password, nni_neighbors_expected)
    list_report = list_report + report_jnpr_lldp

    #report_jnpr_ibgp = audit_jnpr_ibgp(address_ipv4, os_username, os_password, ibgp_peers_expected)
    #list_report = list_report + report_jnpr_ibgp

    return list_report



'''
# To test this function, uncomment this block
####  CONSTANTS  ####
fqdn = 'edge3-testlab.nn.hea.net'
nni_neighbors_expected = [ 'edge1-testlab', 'edge88-testlab' ]
#print(nni_neighbors_expected)
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


report_jnpr_ne_one = audit_jnpr_ne_one(address_ip, local_username, local_password, nni_neighbors_expected)
#print(report_jnpr_ne_one)
for l in report_jnpr_ne_one:
    #print(type(l))
    print(l)
'''
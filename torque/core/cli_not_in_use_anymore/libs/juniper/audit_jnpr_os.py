def audit_jnpr_os(address_ip, os_username, os_password):
    # initialize an empty list, this is what the function will return
    list_report = []

    from jnpr.junos import Device

    device = Device(host=address_ip, user=os_username, password=os_password)
    device.open()

    #print(dir(device.facts))
    #print(device.facts)
  
    os_expected = '16.2R1.6'
    os_expected = '16.2R1.66'
    os_seen = device.facts['version']

    if os_seen == os_expected:
        list_report.append("PASS, you expected OS version " + os_expected + " and you are seeing OS version " + os_seen)
    else:
        list_report.append("FAIL, you expected OS version " + os_expected + " and you are seeing OS version " + os_seen)

    device.close()
    return list_report

# To test this function, uncomment this block
####  CONSTANTS  ####
fqdn = 'edge3-testlab.nn.hea.net'
#print(fqdn)
#nni_neighbors_expected = [ 'edge1-testlab', 'edge88-testlab' ]
local_username = 'heanet'
local_password = 'KqV7X98v!'
#print(local_username)
#print(local_password)
####  CONSTANTS  ####

import sys
import socket
try:
    address_ip = (socket.gethostbyname(fqdn))
    #print(address_ip)
except:
    exit(0)
    e = sys.exc_info()[0]
    print("achung alerta!!")
    print(e)

report_jnpr_os = audit_jnpr_os(address_ip, local_username, local_password)
for l in report_jnpr_os:
    print(l)


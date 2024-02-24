
def audit_jnpr_boilerplate(address_ip, os_username, os_password):

    ''' Initialize, empty, the list that this function will return. '''
    list_report = []


    ''' Import junos-eznc base function and open Netconf session.'''
    from jnpr.junos import Device
    try:
        Device.auto_probe = 5
        device = Device(
            host=address_ipv4,
            user=os_username,
            password=os_password,
            gather_facts=False
        )
        device.open()
    except Exception as err:
        list_report.append("WARNING, the following error has happened: " + str(err))
        return list_report




    try:
        device.close()
    except Exception as err:
        list_report.append("WARNING, the following error has happened: " + str(err))
        return list_report

    return list_report



# mark
####  CONSTANTS  ####
fqdn = 'edge1-testlab.nn.hea.net'
fqdn = 'edge2-testlab.nn.hea.net'
fqdn = 'edge3-testlab.nn.hea.net'
os_username = 'heanet'
os_password = 'KqV7X98v!'


#fqdn = 'core2-dcu.nn.hea.net'
#fqdn = 'edge2-dcu.nn.hea.net'
#fqdn = 'dist2-itb.nn.hea.net'
#fqdn = 'edge1-dcu-spd2.nn.hea.net'
#fqdn = 'edge1-dcu-glasnevin.nn.hea.net'
#os_username = 'rancid'
#os_password = '#pW5MV4G!q%3341sfsdFSS!@'
####  CONSTANTS  ####

#import os
import sys
import socket

try:
    address_ipv4 = (socket.gethostbyname(fqdn))
except:
    exit(0)
    e = sys.exc_info()[0]
    print(e)


audit_report = audit_jnpr_boiler(address_ipv4, os_username, os_password)
for i in audit_report:
    print(i)

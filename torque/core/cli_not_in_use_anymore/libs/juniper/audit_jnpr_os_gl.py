def audit_jnpr_os(address_ip, os_username, os_password):
    # initialize an empty list, this is what the function will return
    list_report = []

    from jnpr.junos import Device

    device = Device(host=address_ip, user=os_username, password=os_password)
    device.open()

#    print(dir(device.facts))
#    print(device.facts)
 
#   print("GATHERING FACTS ABOUT" + hostname)
    hostname = device.facts['hostname']
    model = device.facts['model']
    version = device.facts['version']

    mx104_os_expected = '15.1F6.9'
    mx40_t_os_expected = '15.1F6.9'
    acx5048_os_expected = '15.1X54-D51.7'
    acx2200_os_expected = '16.2R1.6'
    mx960_os_expected = '15.1F6-S1.4'
    mx480_os_expected = '15.1F6-S1.4'
    mx240_os_expected = '15.1F6-S1.4'


#    print(model)
#    print(version)
#    print(hostname)

    print("\nTESTING " + hostname + " " + model) 

    if (model == 'MX40-T' and version == mx40_t_os_expected):
       list_report.append("PASS, EXPECTED:" + " " + mx40_t_os_expected + " " +  "ACTUAL:" + " " + version)
          
    elif (model == 'MX104' and version == mx104_os_expected):
       list_report.append("PASS, EXPECTED:" + " " + mx104_os_expected + " " + "ACTUAL:" + " " + version)

    elif (model == 'ACX5048' and version == acx5048_os_expected):
       list_report.append("PASS, EXPECTED:" + " " + acx5048_os_expected + " " + "ACTUAL:" + " " + version)

    elif (model == 'ACX2200' and version == acx2200_os_expected):
       list_report.append("PASS, EXPECTED:" + " " + acx2200_os_expected + " " + "ACTUAL:" + " " + version)

    elif (model == 'MX960' and version == mx960_os_expected):
       list_report.append("PASS, EXPECTED:" + " " + mx960_os_expected + " " + "ACTUAL:" + " " + version)
    
    elif (model == 'MX480' and version == mx480_os_expected):
       list_report.append("PASS, EXPECTED:" + " " + mx480_os_expected + " " + "ACTUAL:" + " " + version)

    elif (model == 'MX240' and version == mx240_os_expected):
       list_report.append("PASS, EXPECTED:" + " " + mx240_os_expected + " " + "ACTUAL:" + " " + version)
    
    else:
       list_report.append("FAIL, " + hostname + " " + model + " " + "EXPECTED:" + " " + version)
   
#    os_seen = device.facts['version']

#    if os_seen == os_expected:
#        list_report.append("PASS, you expected OS version " + os_expected + " and you are seeing OS version " + os_seen)
#    else:
#        list_report.append("FAIL, you expected OS version " + os_expected + " and you are seeing OS version " + os_seen)

    device.close()
    return list_report

# To test this function, uncomment this block
####  CONSTANTS  ####
fqdn = ['edge1-testlab.nn.hea.net', 'edge2-testlab.nn.hea.net', 'edge3-testlab.nn.hea.net']
#print(fqdn)
local_username = 'heanet'
local_password = 'KqV7X98v!'
#print(local_username)
#print(local_password)
####  CONSTANTS  ####

import sys
import socket

for router in fqdn:
#    print(router)
    try:
        address_ip = (socket.gethostbyname(router))
#        print(address_ip)
    except:
        exit(0)
        e = sys.exc_info()[0]
        print(e)

    report_jnpr_os = audit_jnpr_os(address_ip, local_username, local_password)
    for l in report_jnpr_os:
        print(l)


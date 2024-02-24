
def audit_jnpr_chassis_alarms(address_ipv4, os_username, os_password):
    ''' Return list of test results for Active Chassis Alarms in a Ne.

    Args:
        address_ip (str)
        os_username (str)
        os_password (str)

    Returns:
        list: each item in the list is a line of text. Each line of text begins
        with either of the keywords: PASS, FAIL, or WARNING. These first
        keywords are always in capital letters.

    Requires:
        Python 3.5.2 (or higher)
        junos-eznc 2.1.3 (or higher)

    To-do:
        - if there is 1 alarm, display what the actual alarm is, e.g.:
            Alarm time               Class  Description
            2017-06-29 15:34:11 IST  Major  FPC 1 Major Errors
        - bug in ACX5048, they go ballistic if interrogated with /{'format': 'json'}/
        - improve speed of this function. Invenstigate to retrieve in lxml
          and find/findall with etree
    '''

    ''' Initialize, empty, the list that the function will return. '''
    list_report = []

    ''' Import junos-eznc base function and open Netconf session. '''
    from jnpr.junos import Device
    try:
        Device.auto_probe = 5
        device = Device(host=address_ipv4, user=os_username, password=os_password, gather_facts=False)
        device.open()
    except Exception as err:
        list_report.append("WARNING, the following error has happened: " + str(err))
        return list_report

    #print("Next is device.facts['RE0']['model']")
    #print(device.facts['RE0']['model'])
    #if 'ACX5K' in device.facts['RE0']['model']:
    #    list_report.append("WARNING, do not audit OS for ACX5048 for the moment.")
    #    device.close()
    #    return list_report

    ''' Find out what type of chassis we are dealing with '''
    from lxml import etree
    chassis_inventory = device.rpc.get_chassis_inventory()
    for element in chassis_inventory.findall('.//chassis'):
        chassis_description = element.find('description').text

    ''' If the device is an ACX5048, terminate the function '''
    if (chassis_description == 'ACX5048'):
        list_report.append("WARNING, do not audit OS for ACX5048 for the moment.")
        device.close()
        return list_report


    ''' Retrieve information. '''
    chassis_alarms = device.rpc.get_alarm_information({'format': 'json'})
    # the ACX5048 go ballistic if you put the /{'format': 'json'}/ part!!!
    # smells like a big fat bug!


    ''' 
    The Ne will respond with a dictionary. If there NO alarms, it will have
    a 'no-active-alarms' key, and if there ARE alarms it will have an
    'active-alarm-count' key. These keys are mutually exclusive.
    '''
    alarm_summary = chassis_alarms['alarm-information'][0]['alarm-summary'][0]
    if 'no-active-alarms' in alarm_summary:
        list_report.append("PASS, there are no active chassis alarms.") 
    elif 'active-alarm-count' in alarm_summary:
        # alarm_count is type str
        alarm_count = chassis_alarms['alarm-information'][0]['alarm-summary'][0]['active-alarm-count'][0]['data']
        if alarm_count == '1':
            list_report.append("FAIL, there is " + alarm_count + " active chassis alarm.")
        else:
            list_report.append("FAIL, there are " + alarm_count + " active chassis alarms.")
    else:
        list_report.append("WARNING, can't ascertain if there are alarms or not.")

    device.close()
    return list_report


'''
# mark
# To test this function, uncomment this block
####  CONSTANTS  ####
#fqdn = 'edge1-testlab.nn.hea.net'
#fqdn = 'edge2-testlab.nn.hea.net'
fqdn = 'edge3-testlab.nn.hea.net'
local_username = 'heanet'
local_password = 'KqV7X98v!'

#fqdn = 'edge4-testlab.nn.hea.net'
#fqdn = 'edge5-testlab.nn.hea.net'
#local_username = 'heanet'
#local_password = '$!3u$uxqDMTXzw9'

#fqdn = 'edge1-dcu-glasnevin.nn.hea.net'
#fqdn = 'edge1-dcu-spd2.nn.hea.net'  # device.facts['RE0']['model']
#fqdn = 'edge2-dcu.nn.hea.net'
#fqdn = 'dist1-lyit2.nn.hea.net'
#fqdn = 'rr1-pw.nn.hea.net'
#fqdn = 'core2-blanch.nn.hea.net'
#fqdn = 'core2-pw.nn.hea.net'
#local_username = 'rancid'
#local_password = '#pW5MV4G!q%3341sfsdFSS!@'
####  CONSTANTS  ####

import socket
try:
    address_ipv4 = (socket.gethostbyname(fqdn))
except Exception as err:
    print(str(err))

audit_report = audit_jnpr_chassis_alarms(address_ipv4, local_username, local_password)
for i in audit_report:
    print(i)
'''

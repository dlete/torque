
def audit_jnpr_chassis_alarms(address_ipv4, os_username, os_password, chassis_alarms):
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
        Nothing
    '''

    ''' Initialize, empty, the list that the function will return. '''
    list_report = []

    ''' Import junos-eznc base function and open Netconf session. '''
    from jnpr.junos import Device
    try:
        Device.auto_probe = 5
        device = Device(host=address_ipv4, user=os_username, password=os_password)
        device.open(gather_facts=False)
    except Exception as err:
        list_report.append("WARNING, the following error has happened: " + str(err))
        return list_report

    ''' Retrieve information. '''
    chassis_alarms = device.rpc.get_alarm_information({'format': 'json'})

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
fqdn = 'edge3-testlab.nn.hea.net'
local_username = 'heanet'
local_password = 'KqV7X98v!'

fqdn = 'core1-cork1.nn.hea.net'
local_username = 'rancid'
local_password = '#pW5MV4G!q%3341sfsdFSS!@'
####  CONSTANTS  ####
import os 
import sys
import socket

chassis_alarms = []

try:
    address_ip = (socket.gethostbyname(fqdn))
except:
    exit(0)
    e = sys.exc_info()[0]
    print(e)

report_jnpr_chassis_alarms = audit_jnpr_chassis_alarms(address_ip, local_username, local_password, chassis_alarms)
for l in report_jnpr_chassis_alarms:
    print(l)
'''
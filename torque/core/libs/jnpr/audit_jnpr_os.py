def audit_jnpr_os(address_ip, os_username, os_password):
    '''Return list of test results for Operating System.

    Args:
        address_ip (str)
        os_username (str)
        os_password (str)

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
            host=address_ip,
            user=os_username,
            password=os_password,
            gather_facts=False)
        device.open()
    except Exception as err:
        list_report.append("WARNING, the following error has happened: " + str(err))
        return list_report


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


    #print("GATHERING FACTS ABOUT" + hostname)
    hostname = device.facts['hostname']
    model = device.facts['model']
    version = device.facts['version']


    '''
    This is the authoritative data.
    This is the Baseline to compare against.
    '''
    #mx104_os_expected = '15.1F6.9'
    mx104_os_expected = '16.2R2.8'
    mx40_t_os_expected = '15.1F6.9'
    acx5048_os_expected = '15.1X54-D51.7'
    #acx2200_os_expected = '16.2R2.8'
    acx2200_os_expected = '17.3R3-S1.5'
    #mx240_os_expected = '15.1F6-S1.4'
    mx240_os_expected = '16.2R2.8'
    #mx480_os_expected = '15.1F6-S1.4'
    mx480_os_expected = '16.2R2.8'
    #mx960_os_expected = '15.1F6-S1.4'
    mx960_os_expected = '16.2R2.8'



    if (model == 'MX40-T' and version == mx40_t_os_expected):
       list_report.append("PASS, expected JUNOS OS: " + mx40_t_os_expected + ". Seen: " + version)
          
    elif (model == 'MX104' and version == mx104_os_expected):
       list_report.append("PASS, expected JUNOS OS: " + mx104_os_expected + ". Seen: " + version)

    elif 'ACX5K' in device.facts['RE0']['model']:
        # ACX5048 do not report the JUNOS version they run!!
        # smells like a big fat bug!!!!
        list_report.append("WARNING, do not audit OS for ACX5048 for the moment.")

    elif ('ACX5K' in device.facts['RE0']['model'] and version == acx5048_os_expected):
        list_report.append("PASS, expected JUNOS OS: " + acx5048_os_expected + ". Seen: " + version)

    elif (model == 'ACX2200' and version == acx2200_os_expected):
       list_report.append("PASS, expected JUNOS OS: " + acx2200_os_expected + ". Seen: " + version)

    elif (model == 'MX960' and version == mx960_os_expected):
       list_report.append("PASS, expected JUNOS OS: " + mx960_os_expected + ". Seen: " + version)
    
    elif (model == 'MX480' and version == mx480_os_expected):
       list_report.append("PASS, expected JUNOS OS: " + mx480_os_expected + ". Seen: " + version)

    elif (model == 'MX240' and version == mx240_os_expected):
       list_report.append("PASS, expected JUNOS OS: " + mx240_os_expected + ". Seen: " + version)
    
    else:
       list_report.append("FAIL, " + hostname + " " + model + " " + "EXPECTED: " + version)
   

    device.close()
    return list_report


'''
# mark
# To test this function, uncomment this block
####  CONSTANTS  ####
#fqdn = 'edge1-testlab.nn.hea.net'
#fqdn = 'edge2-testlab.nn.hea.net'
fqdn = 'edge3-testlab.nn.hea.net'
#list_of_fqdn = ['edge1-testlab.nn.hea.net', 'edge2-testlab.nn.hea.net', 'edge3-testlab.nn.hea.net']
local_username = 'heanet'
local_password = 'KqV7X98v!'

#fqdn = 'edge4-testlab.nn.hea.net'
#fqdn = 'edge5-testlab.nn.hea.net'
#list_of_fqdn = ['edge4-testlab.nn.hea.net', 'edge5-testlab.nn.hea.net']
#local_username = 'heanet'
#local_password = '$!3u$uxqDMTXzw9'

#fqdn = 'edge1-dcu-glasnevin.nn.hea.net'
#fqdn = 'edge1-dcu-spd2.nn.hea.net'
#fqdn = 'edge2-dcu.nn.hea.net'
fqdn = 'edge1-nuig-gweedore.nn.hea.net'
#fqdn = 'dist1-lyit2.nn.hea.net'
#fqdn = 'rr1-pw.nn.hea.net'
#fqdn = 'core2-blanch.nn.hea.net'
#fqdn = 'core2-pw.nn.hea.net'
#list_of_fqdn = [ 'edge1-dcu-glasnevin.nn.hea.net', 'edge1-dcu-spd2.nn.hea.net', 'dist1-lyit2.nn.hea.net', 'rr1-pw.nn.hea.net', 'core2-blanch.nn.hea.net', 'core2-pw.nn.hea.net']
local_username = 'rancid'
local_password = '#pW5MV4G!q%3341sfsdFSS!@'
####  CONSTANTS  ####

def audit_one(fqdn, local_username, local_password):
    try:
        import socket
        address_ip = (socket.gethostbyname(fqdn))
    except Exception as err:
        print(str(err))

    audit_report = audit_jnpr_os(address_ip, local_username, local_password)
    for i in audit_report:
        print(i)

audit_one(fqdn, local_username, local_password)

#for fqdn in list_of_fqdn:
#    audit_one(fqdn, local_username, local_password)
'''


'''
# THESE ARE THE FACTS OF AN ACX5K!!!!!!!!!!!!!!!!!!!
{'2RE': False,
 'HOME': '/var/home/remote',
 'RE0': {'last_reboot_reason': '0x1:power cycle/failure',
         'mastership_state': 'master',
         'model': 'ACX5K Routing Engine',
         'status': 'OK',
         'up_time': '55 days, 22 hours, 18 minutes, 28 seconds'},
 'RE1': None,
 'RE_hw_mi': None,
 'current_re': ['master',
                'node',
                'fwdd',
                'member',
                'pfem',
                're0',
                'fpc0',
                'feb0',
                'fpc16'],
 'domain': 'nn.hea.net',
 'fqdn': None,
 'hostname': None,
 'hostname_info': None,
 'ifd_style': 'CLASSIC',
 'junos_info': None,
 'master': 'RE0',
 'model': None,
 'model_info': None,
 'personality': None,
 're_info': {'default': {'0': {'last_reboot_reason': '0x1:power cycle/failure',
                               'mastership_state': 'master',
                               'model': 'ACX5K Routing Engine',
                               'status': 'OK'},
                         'default': {'last_reboot_reason': '0x1:power '
                                                           'cycle/failure',
                                     'mastership_state': 'master',
                                     'model': 'ACX5K Routing Engine',
                                     'status': 'OK'}}},
 're_master': {'default': '0'},
 'serialnumber': None,
 'srx_cluster': None,
 'srx_cluster_id': None,
 'srx_cluster_redundancy_group': None,
 'switch_style': 'VLAN_L2NG',
 'vc_capable': True,
 'vc_fabric': False,
 'vc_master': '0',
 'vc_mode': 'Enabled',
 'version': None,
 'version_RE0': None,
 'version_RE1': None,
 'version_info': None,
 'virtual': None}
'''
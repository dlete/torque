
def audit_jnpr_phyport_stability(address_ip, os_username, os_password):
    '''Return list of test results for Physical ports uptime.

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
        to the Device
    '''

    ''' Initialize, empty, the list that the function will return. '''
    list_report = []

    from jnpr.junos import Device
    try:
        Device.auto_probe = 5
        device = Device(host=address_ip, user=os_username, password=os_password, gather_facts=False)
        device.open()
    except Exception as err:
        list_report.append("WARNING, the following error has happened: " + str(err))
        return list_report

    from jnpr.junos.factory.factory_loader import FactoryLoader
    import yaml
    yaml_data = \
    """
---
MyPhyPortStatsTable:
  rpc: get-interface-information
  args:
    extensive: True
    interface_name: '[efgx][et]-*'
  args_key: interface_name
  item: physical-interface
  view: MyPhyPortStatsView

MyPhyPortStatsView:
  fields:
    description: description
    statistics_cleared: statistics-cleared
    """

    globals().update(FactoryLoader().load(yaml.load(yaml_data)))
    phy_ports_stats = MyPhyPortStatsTable(device).get()

    from datetime import datetime
    #print(phy_ports_stats)
    for p in phy_ports_stats:
        #print("key")
        #print(p.key)
        #print(type(p.key))
        #print("description")
        #print(p.description)
        #print("statistics_cleared")
        #print(p.statistics_cleared)     # 2017-05-23 15:55:29 IST (4w0d 21:22 ago)
        #print(type(p.statistics_cleared))
        #last_cleared_no_tz= p.statistics_cleared.split(' IST')[0]
        #print("last_cleared_no_tz")
        #print(last_cleared_no_tz)                 # 2017-05-23 15:55:29
        #print(type(last_cleared_no_tz))
        #last_cleared = datetime.strptime(last_cleared_no_tz, '%Y-%m-%d %H:%M:%S')
        #print("last_cleared no tz")
        #print(last_cleared)
        #print(type(last_cleared))
        '''
        # with the TIMEZONE does NOT WORK
        last_cleared_tz = p.statistics_cleared.split('(')[0]
        print("last_cleared_tz")
        print(last_cleared_tz)          # # 2017-05-23 15:55:29 IST
        print(type(last_cleared_tz))
        last_cleared = datetime.strptime(last_cleared_tz, '%Y-%m-%d %H:%M:%S %Z')
        print("last_cleared tz")
        print(last_cleared)
        print(type(last_cleared))
        '''

    # The stability period is x days
    number_of_days = 1
    stability_period = number_of_days * (24*60*60)

    # Current time
    time_currently = datetime.now()

    for port in phy_ports_stats:
        # TEST, counters have been running for more than <number_of_days> (e.g. 7) days
        counters_last_cleared = port.statistics_cleared

        if counters_last_cleared == 'Never':
            #print("Next is counters_last_cleared when output is 'Never'")
            #print(counters_last_cleared)
            list_report.append("PASS, statistics counters in port " + port.key +
                " have Never been cleared")
            continue
        else:
            #print("Next is counters_last_cleared when output is any other than 'Never'")
            #print(counters_last_cleared)

            #counters_last_cleared = port.statistics_cleared.split(' IST')[0]
            import re
            #counters_last_cleared = re.split(' IST| GMT', port.statistics_cleared)[0]
            counters_last_cleared = re.split(' [A-Z]', port.statistics_cleared)[0]

            counters_last_cleared = datetime.strptime(counters_last_cleared, '%Y-%m-%d %H:%M:%S')
            #print("counters_last_cleared")
            #print(counters_last_cleared)

        delta_time = time_currently - counters_last_cleared
        #print("delta_time")
        #print(delta_time)
        #print(type(delta_time))
        delta_seconds = delta_time.total_seconds()
        delta_seconds = int(delta_seconds)

        if delta_seconds > stability_period:
            list_report.append("PASS, counters in port " + port.key + 
                " have been running for longer than " + str(number_of_days) + 
                " days. " + "Counters were last cleared on " + str(counters_last_cleared).split(".")[0]
            )
        else:
            list_report.append("FAIL, counters in port " + port.key +
                " have not been running for longer than " + str(number_of_days) +
                " days. " + "Counters were last cleared on " + str(counters_last_cleared).split(".")[0]
            )

    device.close()
    return list_report


'''
# mark
####  CONSTANTS  ####
#fqdn = 'edge1-testlab.nn.hea.net'
#fqdn = 'edge2-testlab.nn.hea.net'
#fqdn = 'edge3-testlab.nn.hea.net'
#local_username = 'heanet'
#local_password = 'KqV7X98v!'

#fqdn = 'edge4-testlab.nn.hea.net'
#fqdn = 'edge5-testlab.nn.hea.net'
#local_username = 'heanet'
#local_password = '$!3u$uxqDMTXzw9'

#fqdn = 'edge1-dcu-glasnevin.nn.hea.net'
#fqdn = 'edge1-dcu-spd2.nn.hea.net'
#fqdn = 'edge2-dcu.nn.hea.net'
fqdn = 'dist1-itb.nn.hea.net'
fqdn = 'dist2-itb.nn.hea.net'
#fqdn = 'dist1-lyit2.nn.hea.net'
#fqdn = 'rr1-pw.nn.hea.net'
#fqdn = 'core2-blanch.nn.hea.net'
#fqdn = 'core2-pw.nn.hea.net'
local_username = 'rancid'
local_password = '#pW5MV4G!q%3341sfsdFSS!@'
####  CONSTANTS  ####

import socket
address_ipv4 = (socket.gethostbyname(fqdn))
#address_ipv6 = socket.getaddrinfo(fqdn, None, socket.AF_INET6)[0][4][0]

audit_report = audit_jnpr_phyport_stability(address_ipv4, local_username, local_password)
for i in audit_report:
    print(i)
'''

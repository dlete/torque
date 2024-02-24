
def audit_jnpr_duplicate_ip(address_ip, os_username, os_password):
    ''' Return a list of test results for duplicate IP addresses

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
        Include UNI links
        Modify so that the function allows to check for an individual prefix.

    It does check that:
        NNI
        /32 appear once (1) in the IS-IS LSDB.
        /31 appear twice (2) in the IS-IS LSDB.
        /30 must not appear (that is zero times) in the IS-IS LSDB.
        /128 appear once (1) in the IS-IS LSDB.
        /127 appear twice (2) in the IS-IS LSDB.

        UNI
        /31, if zero (0) in the IS-IS LSDB => the the RR must have the prefix as active, and protocol next hop be the loopback of the audited NE.
        /30, if zero (0) in the IS-IS LSDB => the the RR must have the prefix as active, and protocol next hop be the loopback of the audited NE.

    It does not check:
        Prefixes other than /32, /31 or /30
        Prefixes other than /128 or /127
        A given prefix is orphan in two non-connected NE; e.g. NE-A is not connected to NE-B, NE-A announces prefix P in IS-IS and NE-B announces the 
            same prefix P in IS-IS. Because each NE-A and NE-B announce P once each, the prefix P appears twice (1 + 1 = 2) in the IS-IS LSDB.
    '''

    ''' Here we only sets/not logging '''
    import logging
    logger = logging.getLogger(__name__)
    # Set to INFO if you do WANT to see DEBUG and INFO messages.
    # Set to WARNING if you do NOT WANT to see DEBUG and INFO messages.
    logging.basicConfig(level=logging.WARNING)


    ''' Initialize, empty, the list that this function will return. '''
    list_report = []


    ''' Import Juniper package junos-eznc and open Netconf session to the NE.'''
    from jnpr.junos import Device
    try:
        Device.auto_probe = 5
        device = Device(
            host=address_ip, 
            user=os_username, 
            password=os_password, 
            gather_facts=False,
            normalize=True)
        device.open()
    except Exception as err:
        list_report.append("WARNING, the following error has happened: " + str(err))
        return list_report


    ''' The Juniper does return the information in XML (C'est la vie!). '''
    from lxml import etree



    ''' Interrogate the NE and put all the, IPv4, Direct, prefixes in a list. '''
    prefixes_ipv4_ne = []
    route_direct_inet_0 = device.rpc.get_route_information(table='inet.0', protocol='direct')
    logger.info('What follows are all the IPv4 Direct prefixes in the NE (rt-destination tag in JUNOS XML).')
    for element in route_direct_inet_0.findall('.//rt-destination'):
        logger.info('rt-destination is: %s', element.text)
        prefixes_ipv4_ne.append(element.text)
    logger.info('There are %s IPv4 Direct prefixes in this NE, stored in the list prefixes_ipv4_ne', len(prefixes_ipv4_ne))

    ''' Interrogate the NE and put all the, IPv6, Direct, prefixes in a list. '''
    prefixes_ipv6_ne = []
    route_direct_inet_6_0 = device.rpc.get_route_information(table='inet6.0', protocol='direct')
    logger.info('What follows are all the IPv6 Direct prefixes in the NE (rt-destination tag in JUNOS XML).')
    logger.info('Only keep IPv6 Direct prefixes of the form "2001:770", do NOT keep Link Local prefixes.')
    for element in route_direct_inet_6_0.findall('.//rt-destination'):
        logger.info('rt-destination is: %s', element.text)
        if '2001:770' in element.text:
            prefixes_ipv6_ne.append(element.text)
    logger.info('There are %s IPv6 Direct prefixes in this NE, stored in the list prefixes_ipv6_ne', len(prefixes_ipv6_ne))



    ''' We will put all the IS-IS database IPv4 prefixes in a list.'''
    prefixes_ipv4_database = []
    ''' We will put all the IS-IS database IPv6 prefixes in a list.'''
    prefixes_ipv6_database = []
    ''' Interrogate the NE for a dump of the IS-IS database. '''
    isis_database_extensive = device.rpc.get_isis_database_information(extensive=True)
    #print(etree.tostring(isis_database_extensive, encoding='unicode'))
    ''' In the dump of the IS-IS database, find all the NE, that is an "isis-database-entry" tag for each NE.'''
    for element in isis_database_extensive.findall('.//isis-database-entry'):
        ''' The NE hostname has the tag "lsp-id".'''
        lsp_id = element.find('.//lsp-id').text
        #logger.info('lsp-id is: %s', lsp_id)

        ''' Prefixes of an NE are all under their own individual "isis-prefix" tag.'''
        for sub in element.findall('.//isis-prefix'):
            protocol_name = sub.find('.//protocol-name').text
            #logger.info('protocol-name is: %s', protocol_name)
            address_prefix = sub.find('.//address-prefix').text
            #logger.info('address_prefix is: %s', address_prefix)
            prefix_flag = sub.find('.//prefix-flag').text
            prefix_status = sub.find('.//prefix-status').text
            if protocol_name == 'IP':
                prefixes_ipv4_database.append(address_prefix)
            if protocol_name == 'V6':
                prefixes_ipv6_database.append(address_prefix)
    #logger.info('these are the IPv4 prefixes in the database: %s', prefixes_ipv4_database)
    #logger.info('these are the IPv6 prefixes in the database: %s', prefixes_ipv6_database)




    ''' Iterate through the list of IPv4 Direct prefixes, prefixes_ipv4_ne and count the number of times the prefix is in the database.'''
    facility_ipv4 = [ '87.44.49.254/32' ]
    prefixes_ipv4_not_in_isis = []
    for ip_prefix in prefixes_ipv4_ne:
        instances = prefixes_ipv4_database.count(ip_prefix)
        logger.info('The IPv4 Direct prefix {} is {} times in the database'.format(ip_prefix, instances))

        if ip_prefix in facility_ipv4:
            pass
        elif '/32' in ip_prefix:
            #logger.info('this prefix is a /32: %s', ip_prefix)
            if instances == 1:
                list_report.append("PASS, prefix " + ip_prefix + 
                    " is correct. It is once (" + 
                    str(instances) + 
                    ") in the database."
                )
                ne_loopback_ipv4 = ip_prefix.split('/')[0]
            else:
                list_report.append("FAIL, prefix " + ip_prefix + 
                    " is incorrect. It is " + 
                    str(instances) + 
                    " times in the database."
                )
        elif '/31' in ip_prefix:
            #logger.info('this prefix is a /31: %s', ip_prefix)
            if instances == 2:
                list_report.append("PASS, prefix " + ip_prefix + " is correct. It is twice (" + str(instances) + ") in the database.")
            elif instances == 0:
                logger.info('This prefix appears 0 times in the database, most probably is a UNI: %s', ip_prefix)
                prefixes_ipv4_not_in_isis.append(ip_prefix)
                pass
            else:
                list_report.append("FAIL, prefix " + ip_prefix + " is incorrect. It is " + str(instances) + " times in the database.")
        elif '/30' in ip_prefix:
            if instances == 0:
                prefixes_ipv4_not_in_isis.append(ip_prefix)
                pass
            else:
                list_report.append("FAIL, prefix " + ip_prefix + 
                " is incorrect. It does appear " + str(instances) + 
                " times in the IS-IS database, but is should not be there.")
        else:
            # Do not check any other prefix length (e.g. /29, /26, /24, etc.). 
            pass


    ''' Iterate through the list of IPv6 Direct prefixes, prefixes_ipv4_ne and count the number of times the prefix is in the database.'''
    facility_ipv6 = [ '2001:770:200:0:ffff:ffff:ffff:ffff/128' ]
    prefixes_ipv6_not_in_isis = []
    for ip_prefix in prefixes_ipv6_ne:
        instances = prefixes_ipv6_database.count(ip_prefix)
        logger.info('The IPv6 Direct prefix {} is {} times in the database'.format(ip_prefix, instances))

        if ip_prefix in facility_ipv6:
            pass
        elif '/128' in ip_prefix:
            #logger.info('this prefix is a /128: %s', ip_prefix)
            if instances == 1:
                list_report.append("PASS, prefix " + ip_prefix + " is correct. It is once (" + str(instances) + ") in the database.")
                ne_loopback_ipv6 = ip_prefix.split('/')[0]
            else:
                list_report.append("FAIL, prefix " + ip_prefix + " is incorrect. It is " + str(instances) + " times in the database.")
        elif '/127' in ip_prefix:
            #logger.info('this prefix is a /127: %s', ip_prefix)
            if instances == 2:
                list_report.append("PASS, prefix " + ip_prefix + " is correct. It is twice (" + str(instances) + ") in the database.")
            elif instances == 0:
                logger.info('This prefix appears 0 times in the database, most probably is a UNI: %s', ip_prefix)
                prefixes_ipv6_not_in_isis.append(ip_prefix)
                pass
            else:
                list_report.append("FAIL, prefix " + ip_prefix + " is incorrect. It is " + str(instances) + " times in the database.")
        else:
            pass


    # This is how we do the UNI. If there was a NE Direct prefix not in IS-IS LSDB, then it must be announced by BGP to the RR.
    if len(prefixes_ipv4_not_in_isis) > 0:
        logger.info('There are at least {} IPv4 prefixes, direct, that are not annunced by IS-IS'.format(len(prefixes_ipv4_not_in_isis)))

        try:
            import socket
            #reference_ne = 'edge1-testlab.nn.hea.net'
            reference_ne = 'rr1-pw.nn.hea.net'
            address_ip = (socket.gethostbyname(reference_ne))
            Device.auto_probe = 5
            local_username = 'rancid'
            local_password = '#pW5MV4G!q%3341sfsdFSS!@'
            reference_device = Device(
                host=address_ip,
                #user=os_username,
                #password=os_password,
                user=local_username,
                password=local_password,
                gather_facts=False,
                normalize=True)
            reference_device.open()
        except Exception as err:
            list_report.append("WARNING, the following error has happened: " + str(err))
            return list_report
        
        # Fetch all the prefixes IPv4 (inet.0), active, protocol BGP, /31
        route_inet_0_bgp_active_slash_31 = reference_device.rpc.get_route_information(
            level='detail',
            table='inet.0',
            active_path=True,
            protocol='bgp',
            match_prefix='*/31'
        )

        # Fetch all the prefixes IPv4 (inet.0), active, protocol BGP, /30
        route_inet_0_bgp_active_slash_30 = reference_device.rpc.get_route_information(
            level='detail',
            table='inet.0',
            active_path=True,
            protocol='bgp',
            match_prefix='*/30'
        )


        # aaa
        # Put all the prefixes in inet.0, protocol BGP, active, prefix length 31 in a dictionary of dictionaries.
        dict_of_route_inet_0_bgp_active_slash_31 = {}
        for element in route_inet_0_bgp_active_slash_31.findall('.//rt-destination'):
            rt_destination = element.text
            rt_prefix_length = element.find('..//rt-prefix-length').text
            active_tag = element.find('..//active-tag').text
            protocol_name = element.find('..//protocol-name').text

            protocol_nh = element.find('..//protocol-nh')
            to = protocol_nh.find('.//to').text

            dict_prefix_n = {}
            dict_prefix_n['rt_destination'] = rt_destination
            dict_prefix_n['rt_prefix_length'] = rt_prefix_length
            dict_prefix_n['active_tag'] = active_tag
            dict_prefix_n['protocol_name'] = protocol_name
            dict_prefix_n['to'] = to

            prefix_ip = str(rt_destination) + '/' + rt_prefix_length
            dict_of_route_inet_0_bgp_active_slash_31[prefix_ip] = dict_prefix_n

        #logger.info('Dictionary of dictionaries, for all prefixes in inet.0, protocol bgp, and /31 is: {}'.format(dict_of_route_inet_0_bgp_active_slash_31))



        # Put all the prefixes in inet.0, protocol BGP, active, prefix length 30 in a dictionary of dictionaries.
        dict_of_route_inet_0_bgp_active_slash_30 = {}
        for element in route_inet_0_bgp_active_slash_30.findall('.//rt-destination'):
            rt_destination = element.text
            rt_prefix_length = element.find('..//rt-prefix-length').text
            active_tag = element.find('..//active-tag').text
            protocol_name = element.find('..//protocol-name').text

            protocol_nh = element.find('..//protocol-nh')
            to = protocol_nh.find('.//to').text

            dict_prefix_n = {}
            dict_prefix_n['rt_destination'] = rt_destination
            dict_prefix_n['rt_prefix_length'] = rt_prefix_length
            dict_prefix_n['active_tag'] = active_tag
            dict_prefix_n['protocol_name'] = protocol_name
            dict_prefix_n['to'] = to

            prefix_ip = str(rt_destination) + '/' + rt_prefix_length
            dict_of_route_inet_0_bgp_active_slash_30[prefix_ip] = dict_prefix_n

        #logger.info('Dictionary of dictionaries, for all prefixes in inet.0, protocol bgp, and /30 is: {}'.format(dict_of_route_inet_0_bgp_active_slash_30))


        dict_of_route_inet_0_bgp_active_slash_31_30 = {}
        dict_of_route_inet_0_bgp_active_slash_31_30.update(dict_of_route_inet_0_bgp_active_slash_31)
        dict_of_route_inet_0_bgp_active_slash_31_30.update(dict_of_route_inet_0_bgp_active_slash_30)
        #logger.info('Dictionary of dictionaries, for all prefixes in inet.0, protocol bgp, and /31 or /30 is: {}'.format(dict_of_route_inet_0_bgp_active_slash_31_30))

        # this is only if you want to test
        list_of_directs_zero_in_isis = [ '193.1.246.148/30', '193.1.255.148/30' ]

        for prefix in prefixes_ipv4_not_in_isis:
        #for prefix in list_of_directs_zero_in_isis:
            if prefix in dict_of_route_inet_0_bgp_active_slash_31_30.keys():
                #if ne_loopback_ipv4 == dict_of_route_inet_0_bgp_active_slash_30[prefix]['to']:
                if ne_loopback_ipv4 == dict_of_route_inet_0_bgp_active_slash_31_30[prefix]['to']:
                    list_report.append("PASS, prefix " + prefix + 
                        " is in the RR as BGP active and the protocol next hop (" + 
                        #dict_of_route_inet_0_bgp_active_slash_30[prefix]['to'] + 
                        dict_of_route_inet_0_bgp_active_slash_31_30[prefix]['to'] +
                        ") is the loopback of this NE (" + ne_loopback_ipv4 + ").")
                else:
                    list_report.append("FAIL, the prefix " + prefix + 
                        " is in the RR as BGP active BUT the protocol next hop (" + 
                        #dict_of_route_inet_0_bgp_active_slash_30[prefix]['to'] + 
                        dict_of_route_inet_0_bgp_active_slash_31_30[prefix]['to'] +
                        ") is NOT the loopback of this NE (" + ne_loopback_ipv4 + ").")
            else:
                list_report.append("FAIL, prefix " + prefix + " is NOT in the RR as BGP active.")

        reference_device.close()


    # This is how we do the IPv6 UNI. If there was a NE Direct prefix not in IS-IS LSDB, then it must be announced by BGP to the RR.
    if len(prefixes_ipv6_not_in_isis) > 0:
        logger.info('There are at least {} IPv6 prefixes, direct, that are not annunced by IS-IS'.format(len(prefixes_ipv6_not_in_isis)))

        try:
            import socket
            #reference_ne = 'edge1-testlab.nn.hea.net'
            reference_ne = 'rr1-pw.nn.hea.net'
            address_ip = (socket.gethostbyname(reference_ne))
            Device.auto_probe = 5
            local_username = 'rancid'
            local_password = '#pW5MV4G!q%3341sfsdFSS!@'
            reference_device = Device(
                host=address_ip,
                #user=os_username,
                #password=os_password,
                user=local_username,
                password=local_password,
                gather_facts=False,
                normalize=True)
            reference_device.open()
        except Exception as err:
            list_report.append("WARNING, the following error has happened: " + str(err))
            return list_report

        # Fetch all the prefixes IPv6 (inet.0), active, protocol BGP, /127
        route_inet_6_bgp_active_slash_127 = reference_device.rpc.get_route_information(
            level='detail',
            table='inet6.0',
            active_path=True,
            protocol='bgp',
            match_prefix='*/127'
        )

        # Put all the IPv6 prefixes in inet6.0, protocol BGP, active, prefix length 127 in a dictionary of dictionaries.
        dict_of_route_inet_6_bgp_active_slash_127 = {}
        for element in route_inet_6_bgp_active_slash_127.findall('.//rt-destination'):
            rt_destination = element.text
            rt_prefix_length = element.find('..//rt-prefix-length').text
            active_tag = element.find('..//active-tag').text
            protocol_name = element.find('..//protocol-name').text

            protocol_nh = element.find('..//protocol-nh')
            to = protocol_nh.find('.//to').text

            dict_prefix_n = {}
            dict_prefix_n['rt_destination'] = rt_destination
            dict_prefix_n['rt_prefix_length'] = rt_prefix_length
            dict_prefix_n['active_tag'] = active_tag
            dict_prefix_n['protocol_name'] = protocol_name
            dict_prefix_n['to'] = to

            prefix_ip = str(rt_destination) + '/' + rt_prefix_length
            dict_of_route_inet_6_bgp_active_slash_127[prefix_ip] = dict_prefix_n

        #logger.info('Dictionary of dictionaries, for all IPv6 prefixes in inet6.0, protocol bgp, and /127 is: {}'.format(dict_of_route_inet_6_bgp_active_slash_127))

        for prefix in prefixes_ipv6_not_in_isis:
            if prefix in dict_of_route_inet_6_bgp_active_slash_127.keys():
                if ne_loopback_ipv6 == dict_of_route_inet_6_bgp_active_slash_127[prefix]['to']:
                    list_report.append("PASS, the prefix " + prefix + " is in the RR as BGP active and the protocol next hop (" + dict_of_route_inet_6_bgp_active_slash_127[prefix]['to'] + ") is the loopback of this NE (" + ne_loopback_ipv6 + ").")
                else:
                    list_report.append("FAIL, the prefix " + prefix + " is in the RR as BGP active BUT the protocol next hop (" + dict_of_route_inet_6_bgp_active_slash_127[prefix]['to'] + ") is NOT the loopback of this NE (" + ne_loopback_ipv6 + ").")
            else:
                list_report.append("FAIL, prefix " + prefix + " is NOT in the RR as BGP active.")


        reference_device.close()



    device.close()
    return list_report

'''
# mark
# To test this function, uncomment this block
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
#fqdn = 'edge1-dcu-spd2.nn.hea.net'  # device.facts['RE0']['model']
#fqdn = 'edge2-dcu.nn.hea.net'
#fqdn = 'dist1-lyit2.nn.hea.net'
#fqdn = 'rr1-pw.nn.hea.net'
#fqdn = 'core1-blanch.nn.hea.net'
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

#address_ipv4 = '193.1.255.255'
#local_username = 'heanet'
#local_password = 'KqV7X98v!'

audit_report = audit_jnpr_duplicate_ip(address_ipv4, local_username, local_password)
for i in audit_report:
    print(i)
'''



'''
heanet@edge3-testlab> show route protocol bgp match-prefix */30 table inet.0 active-path | display xml rpc
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/17.2R2/junos">
    <rpc>
        <get-route-information>
                <table>inet.0</table>
                <active-path/>
                <protocol>bgp</protocol>
                <match-prefix>*/30</match-prefix>
        </get-route-information>
    </rpc>
    <cli>
        <banner></banner>
    </cli>
</rpc-reply>

heanet@edge3-testlab>

heanet@edge3-testlab> show route protocol bgp match-prefix */30 table inet.0 active-path | display xml | no-more
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/17.2R2/junos">
    <route-information xmlns="http://xml.juniper.net/junos/17.2R2/junos-routing">
        <!-- keepalive -->
        <route-table>
            <table-name>inet.0</table-name>
            <destination-count>637</destination-count>
            <total-route-count>1041</total-route-count>
            <active-route-count>637</active-route-count>
            <holddown-route-count>0</holddown-route-count>
            <hidden-route-count>0</hidden-route-count>
            <rt junos:style="brief">
                <rt-destination>193.1.31.64/30</rt-destination>
                <rt-entry>
                    <active-tag>*</active-tag>
                    <current-active/>
                    <last-active/>
                    <protocol-name>BGP</protocol-name>
                    <preference>170</preference>
                    <age junos:seconds="3273575">5w2d 21:19:35</age>
                    <med>0</med>
                    <local-preference>400</local-preference>
                    <learned-from>87.44.48.5</learned-from>
                    <as-path>65001 I
                    </as-path>
                    <validation-state>unverified</validation-state>
                    <nh>
                        <selected-next-hop/>
                        <to>87.44.50.59</to>
                        <via>ge-0/1/2.0</via>
                    </nh>
                </rt-entry>
            </rt>
            <rt junos:style="brief">
                <rt-destination>193.1.31.68/30</rt-destination>
                <rt-entry>
                    <active-tag>*</active-tag>
                    <current-active/>
                    <last-active/>
                    <protocol-name>BGP</protocol-name>
                    <preference>170</preference>
                    <age junos:seconds="3273575">5w2d 21:19:35</age>
                    <med>0</med>
                    <local-preference>400</local-preference>
                    <learned-from>87.44.48.5</learned-from>
                    <as-path>65001 I
                    </as-path>
                    <validation-state>unverified</validation-state>
                    <nh>
                        <selected-next-hop/>
                        <to>87.44.50.59</to>
                        <via>ge-0/1/2.0</via>
                    </nh>
                </rt-entry>
            </rt>
            <rt junos:style="brief">
                <rt-destination>193.1.200.40/30</rt-destination>
                <rt-entry>
                    <active-tag>*</active-tag>
                    <current-active/>
                    <last-active/>
                    <protocol-name>BGP</protocol-name>
                    <preference>170</preference>
                    <age junos:seconds="3273575">5w2d 21:19:35</age>
                    <med>0</med>
                    <local-preference>400</local-preference>
                    <learned-from>87.44.48.5</learned-from>
                    <as-path>65180 I
                    </as-path>
                    <validation-state>unverified</validation-state>
                    <nh>
                        <selected-next-hop/>
                        <to>87.44.50.59</to>
                        <via>ge-0/1/2.0</via>
                    </nh>
                </rt-entry>
            </rt>
            <rt junos:style="brief">
                <rt-destination>193.1.200.44/30</rt-destination>
                <rt-entry>
                    <active-tag>*</active-tag>
                    <current-active/>
                    <last-active/>
                    <protocol-name>BGP</protocol-name>
                    <preference>170</preference>
                    <age junos:seconds="3273575">5w2d 21:19:35</age>
                    <local-preference>400</local-preference>
                    <learned-from>87.44.48.5</learned-from>
                    <as-path>65006 I
                    </as-path>
                    <validation-state>unverified</validation-state>
                    <nh>
                        <selected-next-hop/>
                        <to>87.44.50.59</to>
                        <via>ge-0/1/2.0</via>
                    </nh>
                </rt-entry>
            </rt>
            <rt junos:style="brief">
                <rt-destination>193.1.201.0/30</rt-destination>
                <rt-entry>
                    <active-tag>*</active-tag>
                    <current-active/>
                    <last-active/>
                    <protocol-name>BGP</protocol-name>
                    <preference>170</preference>
                    <age junos:seconds="3273575">5w2d 21:19:35</age>
                    <med>0</med>
                    <local-preference>400</local-preference>
                    <learned-from>87.44.48.5</learned-from>
                    <as-path>65136 I
                    </as-path>
                    <validation-state>unverified</validation-state>
                    <nh>
                        <selected-next-hop/>
                        <to>87.44.50.59</to>
                        <via>ge-0/1/2.0</via>
                    </nh>
                </rt-entry>
            </rt>
            <rt junos:style="brief">
                <rt-destination>193.1.246.0/30</rt-destination>
                <rt-entry>
                    <active-tag>*</active-tag>
                    <current-active/>
                    <last-active/>
                    <protocol-name>BGP</protocol-name>
                    <preference>170</preference>
                    <age junos:seconds="3273575">5w2d 21:19:35</age>
                    <med>0</med>
                    <local-preference>400</local-preference>
                    <learned-from>87.44.48.5</learned-from>
                    <as-path>65104 I
                    </as-path>
                    <validation-state>unverified</validation-state>
                    <nh>
                        <selected-next-hop/>
                        <to>87.44.50.59</to>
                        <via>ge-0/1/2.0</via>
                    </nh>
                </rt-entry>
            </rt>
            <rt junos:style="brief">
                <rt-destination>193.1.246.20/30</rt-destination>
                <rt-entry>
                    <active-tag>*</active-tag>
                    <current-active/>
                    <last-active/>
                    <protocol-name>BGP</protocol-name>
                    <preference>170</preference>
                    <age junos:seconds="3273575">5w2d 21:19:35</age>
                    <med>0</med>
                    <local-preference>400</local-preference>
                    <learned-from>87.44.48.5</learned-from>
                    <as-path>65117 I
                    </as-path>
                    <validation-state>unverified</validation-state>
                    <nh>
                        <selected-next-hop/>
                        <to>87.44.50.59</to>
                        <via>ge-0/1/2.0</via>
                    </nh>
                </rt-entry>
            </rt>
            <rt junos:style="brief">
                <rt-destination>193.1.246.144/30</rt-destination>
                <rt-entry>
                    <active-tag>*</active-tag>
                    <current-active/>
                    <last-active/>
                    <protocol-name>BGP</protocol-name>
                    <preference>170</preference>
                    <age junos:seconds="3273575">5w2d 21:19:35</age>
                    <med>0</med>
                    <local-preference>400</local-preference>
                    <learned-from>87.44.48.5</learned-from>
                    <as-path>65104 I
                    </as-path>
                    <validation-state>unverified</validation-state>
                    <nh>
                        <selected-next-hop/>
                        <to>87.44.50.59</to>
                        <via>ge-0/1/2.0</via>
                    </nh>
                </rt-entry>
            </rt>
            <rt junos:style="brief">
                <rt-destination>193.1.246.148/30</rt-destination>
                <rt-entry>
                    <active-tag>*</active-tag>
                    <current-active/>
                    <last-active/>
                    <protocol-name>BGP</protocol-name>
                    <preference>170</preference>
                    <age junos:seconds="3273575">5w2d 21:19:35</age>
                    <local-preference>400</local-preference>
                    <learned-from>87.44.48.5</learned-from>
                    <as-path>65104 I
                    </as-path>
                    <validation-state>unverified</validation-state>
                    <nh>
                        <selected-next-hop/>
                        <to>87.44.50.59</to>
                        <via>ge-0/1/2.0</via>
                    </nh>
                </rt-entry>
            </rt>
        </route-table>
    </route-information>
    <cli>
        <banner></banner>
    </cli>
</rpc-reply>

heanet@edge3-testlab>
'''


def audit_jnpr_ibgp(address_ip, os_username, os_password, peers_expected):
    '''Return list of test results for an iBGP peer.
    
    Taking as input a Ne, and a list of expected iBGP peers, the function
    verifies that the Ne is correctly configured (Administratively) and that
    the status of the iBGP peers is as expected (Operationally).

    Args:
        address_ip (str)
        os_username (str)
        os_password (str)
        peers_expected (list)

    Returns:
        list: each item in the list is a line of text. Each line of text begins
        with either of the keywords: PASS, FAIL, or WARNING. These first
        keywords are always in capital letters.

    Requires:
        Python 3.5.2
        junos-eznc 2.1.3
        PyYAML 3.12

    To-do:: 
        - BGP session has been up for longer than a reference timeperiod.
        - Add error handling. We are not checking what to do if we can't connect
        to the Device
    '''

    import logging
    logger = logging.getLogger(__name__)
    # CHANGE TO INFO IF YOU WANT TO SEE DEBUG AND INFO MESSAGES
    logging.basicConfig(level=logging.WARNING)

    ''' Initialize, empty, the list that the function will return. '''
    list_report = []

    ''' Import junos-eznc base function and open Netconf session. '''
    from jnpr.junos import Device
    try:
        Device.auto_probe = 5
        device = Device(host=address_ip, user=os_username, password=os_password, gather_facts=False)
        device.open()
    except Exception as err:
        list_report.append("WARNING, the following error has happened: " + str(err))
        return list_report

    ''' Find out what type of chassis we are dealing with '''
    from lxml import etree
    chassis_inventory = device.rpc.get_chassis_inventory()
    for element in chassis_inventory.findall('.//chassis'):
        chassis_description = element.find('description').text


    #model = device.facts['model']
    #if (model == 'MX480' or model == 'MX960'):

    # Map of number of IPv4 and IPv6 prefixes to NE model.
    if (chassis_description == 'MX960' or chassis_description == 'MX480'):
        min_prefixes_ipv4 = 400000
        max_prefixes_ipv4 = 750000
        min_prefixes_ipv6 = 35000
        max_prefixes_ipv6 = 50000
        # print("have just seen an MX480 or an MX960")
    else:
        min_prefixes_ipv4 = 350
        max_prefixes_ipv4 = 500
        min_prefixes_ipv6 = 50 
        max_prefixes_ipv6 = 200
        # print("have just seen something that is not an MX480 or an MX960")


    # Map of address families to NE model
    # This is the baseline, the common denominator
    # All NE have at least this collection of address families
    ipv4_safi_expected = ['inet-unicast', 'inet-vpn-unicast',
        'inet-labeled-unicast', 'inet6-vpn-unicast', 'route-target',
        'inet-vpn-flow', 'inet-mvpn', 'inet6-mvpn', 'l2vpn-signaling'
    ]
    #ipv6_safi_expected = ['inet6-unicast', 'inet6-multicast']
    ipv6_safi_expected = ['inet6-unicast']

    if (chassis_description == 'ACX2200'):
        ipv4_safi_expected = ipv4_safi_expected
        # a "pass" would work equally well probably.
    else:
        ipv4_safi_expected.append('evpn')


    ''' Retrieve information. '''
    from jnpr.junos.op.bgp import bgpTable
    peers_seen = bgpTable(device).get()


    from jnpr.junos.factory.factory_loader import FactoryLoader
    import yaml
    yaml_data = \
    """
---
myBgpTable:
 rpc: get-bgp-neighbor-information
 item: bgp-peer
 view: bgpView
 key: peer-id

bgpView:
 fields:
  peer_address: peer-address
  peer_as: peer-as
  local_address: local-address
  local_as: local-as
  peer_group: peer-group
  peer_type: peer-type
  peer_state: peer-state
  authentication_configured: bgp-option-information/authentication-configured
  address_families: bgp-option-information/address-families
  flap_count: flap-count  # how to clear counters?
  peer_id: peer-id
  local_id: local-id
  route_received: bgp-rib/received-prefix-count
   """

    globals().update(FactoryLoader().load(yaml.load(yaml_data)))
    bgp_peers_seen = myBgpTable(device).get()

    
    # testing, begin
    #print(dir(bgp_peers_seen))
    #print(bgp_peers_seen._key_list)
    #print(bgp_peers_seen._keys)
    #print(bgp_peers_seen.key_list)
    #print(bgp_peers_seen.keys)
    #print(bgp_peers_seen.__dict__)
    #print(bgp_peers_seen.values)
    #print(bgp_peers_seen.view)
    '''
    for bgp_peer_seen in bgp_peers_seen:
        #print("bgp_peer_seen.address_families")
        #print(bgp_peer_seen.address_families)
        #print(type(bgp_peer_seen.address_families))
        #af = bgp_peer_seen.address_families.split()
        #print(af)
        #print(type(af))
        #print("bgp_peer_seen.route_received")
        #print(bgp_peer_seen.route_received)
        #print(type(bgp_peer_seen.route_received))
        print("flap_count")
        print(bgp_peer_seen.flap_count)
        print(type(bgp_peer_seen.flap_count))
    '''
    # testing, end
    

    # initialize an empty list, here we will put ALL the BGP peers we see.
    list_peers_seen = []
    # Cleanse and populate the list of BGP Peers seen.
    # Data is presented to us as <ip_address>+<port>, e.g.: 87.44.48.5+61032
    # and we need it as <ip_address>, e.g.: 87.44.48.5
    for bgp_peer_seen in bgp_peers_seen:
        list_peers_seen.append(bgp_peer_seen.peer_address.split('+')[0])


    # TEST, What you expected to see, you see
    for peer_expected in peers_expected:
        if peer_expected in list_peers_seen:
            list_report.append("PASS, you expected to see BGP peer " + peer_expected + " and you are seeing it.")

            for bgp_peer_seen in bgp_peers_seen:
                if peer_expected == bgp_peer_seen.peer_address.split('+')[0]:
                    # TEST, authentication is enabled.
                    if bgp_peer_seen.authentication_configured == "authentication-configured":
                        list_report.append("PASS, you expected to have authentication enabled with BGP peer " +
                            peer_expected + " and authentication is enabled."
                        )
                    else:
                        list_report.append("FAIL, you expected to have authentication enabled with BGP peer " +
                            peer_expected + " and authentication NOT is enabled."
                        )

                    # TEST, BGP session is "Up", BGP session is Established.
                    if bgp_peer_seen.peer_state == "Established":
                        list_report.append("PASS, you expected to see BGP peer " + 
                            peer_expected + 
                            " in Established state and that is the way it is."
                        )
                    else:
                        list_report.append("FAIL, you expected to see BGP peer " + 
                            peer_expected + 
                            " in Established state and it is in " + 
                            bgp_peer_seen.peer_state + " state."
                        )


                    '''
                    # TEST, BGP session has no flaps.
                    if int(bgp_peer_seen.flap_count) < 1:
                        list_report.append("PASS, you expected to have no " +
                            "flaps in the BGP session, and you have " +
                            bgp_peer_seen.flap_count + " flaps.")
                    else:
                        list_report.append("FAIL, you expected to have no " +
                            "flaps in the BGP session, and you have " +
                            bgp_peer_seen.flap_count + " flaps.")
                    '''

                    # Figure if the BGP Peer is an IPv4 address. IPv4 addresses use "." to separate octets.
                    if "." in bgp_peer_seen.peer_address.split('+')[0]:
                        # TEST, the AFI and SAFI are consistent between expected and seen.
                        if ipv4_safi_expected == bgp_peer_seen.address_families.split():
                            list_report.append("PASS, with BGP peer " + peer_expected + " you expected to see the address families " +
                                str(ipv4_safi_expected) + " and you are seeing them all.")
                        else:
                            list_report.append("FAIL, with BGP peer " + peer_expected + " you expected to see the address families " +
                                str(ipv4_safi_expected) + " but you are seeing these instead: " +
                                bgp_peer_seen.address_families
                            )


                        # TEST, the number of prefixes is consistent with what is expected.
                        ipv4_unicast_prefixes_received = int(bgp_peer_seen.route_received[0])

                        #if int(ipv4_unicast_prefixes_received) > min_prefixes_ipv4 and int(ipv4_unicast_prefixes_received) < max_prefixes_ipv4:
                        if min_prefixes_ipv4 < ipv4_unicast_prefixes_received < max_prefixes_ipv4:
                            list_report.append("PASS, from BGP peer " + peer_expected + ", in the address family IPv4 Unicast, " +
                                "you expected to receive between " + str(min_prefixes_ipv4) + " and " + str(max_prefixes_ipv4) + 
                                " prefixes and you are receiving " + str(ipv4_unicast_prefixes_received))
                        else:
                            list_report.append("FAIL, from BGP peer " + peer_expected + ", in the address family IPv4 Unicast, " +
                                "you expected to receive between " + str(min_prefixes_ipv4) + " and " + str(max_prefixes_ipv4) +
                                " prefixes and you are receiving " + str(ipv4_unicast_prefixes_received))


                    # Figure if the BGP Peer is an IPv6 address. IPv6 addresses use ":" to separate hex groups.
                    if ":" in bgp_peer_seen.peer_address.split('+')[0]:
                        # TEST, the AFI and SAFI are consistent between expected and seen.
                        if ipv6_safi_expected == bgp_peer_seen.address_families.split():
                            list_report.append("PASS, with BGP peer " + peer_expected + " you expected to see the address families " +
                                str(ipv6_safi_expected) + " and you are seeing them all.")
                        else:
                            list_report.append("FAIL, with BGP peer " + peer_expected + " you expected to see the address families " +
                                str(ipv6_safi_expected) + " but you are seeing these instead: " +
                                bgp_peer_seen.address_families
                            )


                        # TEST, the number of prefixes is consistent with what is expected.
                        ipv6_unicast_prefixes_received = int(bgp_peer_seen.route_received)
                        if min_prefixes_ipv6 < int(ipv6_unicast_prefixes_received) < max_prefixes_ipv6:
                            list_report.append("PASS, from BGP peer " + peer_expected + ", in the address family IPv6 Unicast, " +
                                "you expected to receive between " + str(min_prefixes_ipv6) + " and " + str(max_prefixes_ipv6) +
                                " prefixes and you are receiving " + str(ipv6_unicast_prefixes_received))
                        else:
                            list_report.append("FAIL, from BGP peer " + peer_expected + ", in the address family IPv6 Unicast, " +
                                "you expected to receive between " + str(min_prefixes_ipv6) + " and " + str(max_prefixes_ipv6) +
                                " prefixes and you are receiving " + str(ipv6_unicast_prefixes_received))


        else:
            list_report.append("FAIL, you expected to see BGP peer " + peer_expected + " but you do not see it.")


    # TEST, What you see, was expected, remember, we are testing iBGP here!!
    # Initialize an empty list, here we will put ALL the iBGP peers we see, notice the "i" in iBGP.
    number_of_ibgp_peers_seen = 0

    for bgp_peer_seen in bgp_peers_seen:
        # We are only interested in the BGP Peer if it is iBGP, if it is "Internal".
        if bgp_peer_seen.peer_type == "Internal":
            # Add +1 to the number of iBGP Peers
            number_of_ibgp_peers_seen = number_of_ibgp_peers_seen + 1

            # TEST, the iBGP Peer we see, we expected to see.
            if bgp_peer_seen.peer_address.split('+')[0] in peers_expected:
                list_report.append("PASS, you see BGP peer " + bgp_peer_seen.peer_address.split('+')[0] + " in BGP AS" +
                    bgp_peer_seen.peer_as + " and that was expected.")
            else:
                list_report.append("FAIL, you see BGP peer " + bgp_peer_seen.peer_address.split('+')[0] + " in BGP AS" +
                    bgp_peer_seen.peer_as + " and that was NOT expected. " )


    # TEST, the NUMBER of BGP peers EXPECTED and SEEN is the SAME
    number_of_peers_expected = peers_expected.__len__()
    if number_of_ibgp_peers_seen == number_of_peers_expected:
        list_report.append("PASS, you expected to see " + str(number_of_peers_expected) + " iBGP peers and you are seeing " +
            str(number_of_ibgp_peers_seen) + " iBGP peers.")
    else:
        list_report.append("FAIL, you expected to see " + str(number_of_peers_expected) + " iBGP peers and you are seeing " +
            str(number_of_ibgp_peers_seen) + " iBGP peers.")



    ##### THIS IS THE STABILITY PART
    ''' Retrieve information. '''
    from jnpr.junos.factory.factory_loader import FactoryLoader
    import yaml
    yaml_data = \
    """
---
myBgpSummaryTable:
  rpc: get-bgp-summary-information
  item: bgp-peer
  view: myBgpSummaryView
  key: peer-address

myBgpSummaryView:
  fields:
    peer_address: peer-address
    peer_as: peer-as
    input_messages: input-messages
    output_messages: output-messages
    route_queue_count: route-queue-count
    flap_count: flap-count
    elapsed_time: elapsed-time
    peer_state: peer-state
    """

    globals().update(FactoryLoader().load(yaml.load(yaml_data)))
    bgp_peers_summary = myBgpSummaryTable(device).get()

    # The stability period is x days
    number_of_days = 5
    stability_period = number_of_days * (24*60*60)

    for bgp_peer in bgp_peers_summary:
        if bgp_peer.peer_as == '1213':
            logger.info('This is an iBGP session')

            # format is: bgp_peer.elapsed_time: 2w4d 10:59:11
            # format is: bgp_peer.elapsed_time: 4d 2:16:33
            if "d" in bgp_peer.elapsed_time:
                wd_section = bgp_peer.elapsed_time.split('d ')[0]
                up_hours_minutes_seconds = bgp_peer.elapsed_time.split('d ')[1]
                if "w" in wd_section:
                    up_weeks = wd_section.split('w')[0]
                    up_days = wd_section.split('w')[1]
                else:
                    up_weeks = 0
                    up_days = wd_section
            else:
                up_weeks = 0
                up_days = 0
                up_hours_minutes_seconds = bgp_peer.elapsed_time

            sec_in_up_weeks = int(up_weeks) * 7 * 24 * 60 * 60
            logger.info('Weeks up: {}'.format(up_weeks))
            logger.info('{} weeks are {} seconds'.format(up_weeks, sec_in_up_weeks))

            #up_days = bgp_peer.elapsed_time.split('d ')[0]
            sec_in_up_days = int(up_days) * 24 * 60 * 60
            logger.info('Days up: {}'.format(up_days))
            logger.info('{} days are {} seconds'.format(up_days, sec_in_up_days))

            #up_hours_minutes_seconds = bgp_peer.elapsed_time.split('d ')[1]
            #logger.info('Hours, Minutes and Seconds up: %s', bgp_peer.elapsed_time.split('d ')[1])
            import time
            try:
                # if we reach this point, days and/or weeks have been removed for us.
                up_hms = time.strptime(up_hours_minutes_seconds, '%H:%M:%S')
            except:
                # you are here because 1 hour has not elapsed yet since the session is up.
                up_hms = time.strptime(up_hours_minutes_seconds, '%M:%S')
            sec_in_h = up_hms.tm_hour * 60 * 60
            logger.info('{} hours are {} seconds'.format(up_hms.tm_hour, sec_in_h))
            sec_in_m = up_hms.tm_min * 60
            logger.info('{} minutes are {} seconds'.format(up_hms.tm_min, sec_in_m))
            sec_in_s = up_hms.tm_sec
            logger.info('{} seconds are {} seconds'.format(up_hms.tm_sec, sec_in_s))
            sec_in_hms = sec_in_h + sec_in_m + sec_in_s
            #logger.info('{} H:M:S are {} seconds'.format(up_hms, sec_in_hms))

            up_seconds = sec_in_up_weeks + sec_in_up_days + sec_in_hms
            logger.info('{} are {} seconds'.format(bgp_peer.elapsed_time, up_seconds))

            if up_seconds > stability_period:
                list_report.append("PASS, BGP stability with " +
                    bgp_peer.peer_address +
                    ". BGP session has been stable for longer than " +
                    str(number_of_days) + " days. BGP session has been " +
                    bgp_peer.peer_state + " for " + bgp_peer.elapsed_time + "."
                )
            else:
                list_report.append("FAIL, BGP stability with " +
                    bgp_peer.peer_address +
                    ". BGP session has not been stable for longer than " +
                    str(number_of_days) + " days. BGP session has been " +
                    bgp_peer.peer_state + " for " + bgp_peer.elapsed_time + "."
                )

        else:
            logger.info('This is NOT an iBGP session')
            pass


    device.close()
    return list_report


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
fqdn = 'edge1-ul-troy.nn.hea.net'
#fqdn = 'edge1-dcu-spd2.nn.hea.net'
#fqdn = 'edge2-dcu.nn.hea.net'
#fqdn = 'dist1-lit2.nn.hea.net'
#fqdn = 'dist1-lyit2.nn.hea.net'
#fqdn = 'rr1-pw.nn.hea.net'
#fqdn = 'core2-blanch.nn.hea.net'
#fqdn = 'core2-pw.nn.hea.net'
local_username = 'heanet'
local_password = '$!3u$uxqDMTXzw9'

ibgp_ipv4_peers_expected = ['87.44.48.5', '87.44.48.6']
ibgp_ipv6_peers_expected = ['2001:770:200::5', '2001:770:200::6']
ibgp_peers_expected = ['87.44.48.5', '87.44.48.6', '2001:770:200::5', '2001:770:200::6']
####  CONSTANTS  ####

import socket
address_ipv4 = (socket.gethostbyname(fqdn))
#address_ipv6 = socket.getaddrinfo(fqdn, None, socket.AF_INET6)[0][4][0]
#print(address_ipv6)
audit_report = audit_jnpr_ibgp(address_ipv4, local_username, local_password, ibgp_peers_expected)
for i in audit_report:
    print(i)

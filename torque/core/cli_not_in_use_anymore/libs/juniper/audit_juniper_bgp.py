
def audit_jnpr_ibgp(address_ip, os_username, os_password, peers_expected):
    '''
    TO DO: filter ONLY iBGP sessions
    '''
    # initialize an empty list, this is what the function will return
    list_report = []

    from jnpr.junos import Device
    device = Device(host=address_ip, user=os_username, password=os_password)
    device.open(gather_facts=False)

    from jnpr.junos.op.bgp import bgpTable
    peers_seen = bgpTable(device).get()

    ipv4_safi_expected = ['inet-unicast', 'inet-vpn-unicast', 
        'inet-labeled-unicast', 'inet6-vpn-unicast', 'route-target', 
        'inet-vpn-flow', 'inet-mvpn', 'inet6-mvpn', 'evpn', 'l2vpn-signaling'
    ]
    ipv6_safi_expected = ['inet6-unicast', 'inet6-multicast']
    number_of_peers_expected = peers_expected.__len__()
    number_of_peers_seen = peers_seen.__len__()

    # TEST, the NUMBER of BGP peers EXPECTED and SEEN is the SAME
    if number_of_peers_seen == number_of_peers_expected:
        list_report.append("PASS, you expected to see " + str(number_of_peers_expected) + " iBGP peers and you are seeing " + 
            str(number_of_peers_seen) + " iBGP peers.")
    else:
        list_report.append("FAIL, you expected to see " + str(number_of_peers_expected) + " iBGP peers and you are seeing " +
            str(number_of_peers_seen) + " iBGP peers.")

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
  # flap_count: flap-count  # how to clear counters?
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
    for bgp_peer_seen in bgp_peers_seen:
        #print("bgp_peer_seen.address_families")
        #print(bgp_peer_seen.address_families)
        #print(type(bgp_peer_seen.address_families))
        #af = bgp_peer_seen.address_families.split()
        #print(af)
        #print(type(af))
        print("bgp_peer_seen.route_received")
        print(bgp_peer_seen.route_received)
        print(type(bgp_peer_seen.route_received))
    # testing, end


    list_peers_seen = []
    for bgp_peer_seen in bgp_peers_seen:
        list_peers_seen.append(bgp_peer_seen.peer_address.split('+')[0])

    # TEST, What you expected to see, you see
    for peer_expected in peers_expected:
        if peer_expected in list_peers_seen:
            list_report.append("PASS, you expected to see BGP peer " + peer_expected + " and you are seeing it.")
            for bgp_peer_seen in bgp_peers_seen:
                if peer_expected == bgp_peer_seen.peer_address.split('+')[0]:
                    if bgp_peer_seen.authentication_configured == "authentication-configured":
                        list_report.append("PASS, you expected to have authentication enabled with BGP peer" +
                            peer_expected + " and authentication is enabled."
                        )
                    else:
                        list_report.append("FAIL, you expected to have authentication enabled with BGP peer" +
                            peer_expected + " and authentication NOT is enabled."
                        )

                    if bgp_peer_seen.peer_state == "Established":
                        list_report.append("PASS, you expected to see BGP peer" + 
                            peer_expected + 
                            " in Established state and that is the way it is."
                        )
                    else:
                        list_report.append("FAIL, you expected to see BGP peer" + 
                            peer_expected + 
                            " in Established state and it is in " + 
                            bgp_peer_seen.peer_state + " state."
                        )

                    if "." in bgp_peer_seen.peer_address.split('+')[0]:
                        if ipv4_safi_expected == bgp_peer_seen.address_families.split():
                            list_report.append("PASS, with BGP peer " + peer_expected + " you expected to see the address families " +
                                str(ipv4_safi_expected) + " and you are seeing them all.")
                        else:
                            list_report.append("FAIL, with BGP peer " + peer_expected + " you expected to see the address families " +
                                str(ipv4_safi_expected) + " but you are seeing these instead: " +
                                bgp_peer_seen.address_families
                            )
                        
                        ipv4_unicast_prefixes_received = bgp_peer_seen.route_received[0]
                        if int(ipv4_unicast_prefixes_received) > 400 and int(ipv4_unicast_prefixes_received) < 500:
                            list_report.append("PASS, from BGP peer " + peer_expected + ", in the address family IPv4 Unicast, " +
                                "you expected to receive between 400 and 500 prefixes and you are receiving " +
                                ipv4_unicast_prefixes_received
                            )
                        else:
                            list_report.append("FAIL, from BGP peer " + peer_expected + ", in the address family IPv4 Unicast, " +
                                "you expected to receive between 400 and 500 prefixes and you are receiving " +
                                ipv4_unicast_prefixes_received
                            )
                        
                    if ":" in bgp_peer_seen.peer_address.split('+')[0]:
                        if ipv6_safi_expected == bgp_peer_seen.address_families.split():
                            list_report.append("PASS, with BGP peer " + peer_expected + " you expected to see the address families " +
                                str(ipv6_safi_expected) + " and you are seeing them all.")
                        else:
                            list_report.append("FAIL, with BGP peer " + peer_expected + " you expected to see the address families " +
                                str(ipv6_safi_expected) + " but you are seeing these instead: " +
                                bgp_peer_seen.address_families
                            )

                        ipv6_unicast_prefixes_received = bgp_peer_seen.route_received[0]
                        print(ipv6_unicast_prefixes_received)
                        if int(ipv6_unicast_prefixes_received) > 0 and int(ipv6_unicast_prefixes_received) < 2:
                            list_report.append("PASS, from BGP peer " + peer_expected + ", in the address family IPv6 Unicast, " +
                                "you expected to receive one (1) prefix and you are receiving " +
                                ipv6_unicast_prefixes_received
                            )
                        else:
                            list_report.append("FAIL, from BGP peer " + peer_expected + ", in the address family IPv6 Unicast, " +
                                "you expected to receive one (1) prefix and you are receiving " +
                                ipv6_unicast_prefixes_received
                            )

        else:
            list_report.append("FAIL, you expected to see BGP peer " + peer_expected + " but you do not see it.")

    # TEST, What you see, was expected
    for bgp_peer_seen in bgp_peers_seen:
        if bgp_peer_seen.peer_address.split('+')[0] in peers_expected:
            list_report.append("PASS, you see BGP peer " + bgp_peer_seen.peer_address.split('+')[0] + " in BGP AS" +
                bgp_peer_seen.peer_as + " and that was expected.")
        else:
            list_report.append("FAIL, you see BGP peer " + bgp_peer_seen.peer_address.split('+')[0] + " in BGP AS" +
                bgp_peer_seen.peer_as + " and that was NOT expected. " )

    device.close()
    return list_report

'''
# To test this function, uncomment this block
####  CONSTANTS  ####
fqdn = 'edge3-testlab.nn.hea.net'
nni_neighbors_expected = [ 'edge1-testlab', 'edge88-testlab' ]
#print(nni_neighbors_expected)
ibgp_ipv4_peers_expected = ['87.44.48.5', '87.44.48.6']
#print(ibgp_ipv4_peers_expected)
ibgp_ipv6_peers_expected = ['2001:770:200::5', '2001:770:200::6']
#print(ibgp_ipv6_peers_expected)

ibgp_peers_expected = ['87.44.48.5', '87.44.48.6', '2001:770:200::5', '2001:770:200::6']
local_username = 'heanet'
local_password = 'KqV7X98v!'
####  CONSTANTS  ####

import socket
address_ipv4 = (socket.gethostbyname(fqdn))
address_ipv6 = socket.getaddrinfo(fqdn, None, socket.AF_INET6)[0][4][0]
#print(address_ipv6)
blah = audit_jnpr_ibgp(address_ipv4, local_username, local_password, ibgp_peers_expected)
blah.insert(0, fqdn + "  ********  iBGP audit report, begin  ********")
blah.append(fqdn + "  ********  iBGP audit report, end  ********")
for i in blah:
    print(i)
'''

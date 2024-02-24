
def audit_jnpr_phyport(address_ip, os_username, os_password):
    '''Return list of test results for Physical ports.

    Args:
        address_ip (str)
        os_username (str)
        os_password (str)

    Returns:
        list: each item in the list is a line of text. Each line of text begins$
        with either of the keywords: PASS, FAIL, or WARNING. These first$
        keywords are always in capital letters.

    Requires:
        Python 3.5.2
        junos-eznc 2.1.3

    To-do:
        Add error handling. We are not checking what to do if we can't connect
        to the Device.
        Add more rx/tx errors, if there are any that respond.
    '''


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

    ''' Retrieve information. '''
    from jnpr.junos.op.phyport import PhyPortTable
    #from jnpr.junos.op.phyport import PhyPortStatsTable
    from jnpr.junos.op.phyport import PhyPortErrorTable
    phyPorts = PhyPortTable(device).get()
    phyPortsErrors = PhyPortErrorTable(device).get()

    '''
    # TEST, Administrative and Operational status are consistent.
    for p in phyPorts:
        #print(p.key)
        if p.oper == p.admin:
            list_report.append("PASS, port " + p.key + " Administrative and " +
                "Operational status are the same. Both are in " + p.oper +
                " status."
            )
        else:
            list_report.append("FAIL, port " + p.key + " Administrative and " +
                "Operational status are NOT the same. Port " + p.key +  
                " is Administratively " + p.admin + ", but Operationally " + 
                p.oper + "."
            )
    '''
    '''
    # TEST, if it is Admin up it must have a description
    for p in phyPorts:
        if p.admin == "up":
            if p.description is None:
                list_report.append("FAIL, port " + p.key + " is Administratively " + p.admin +
                    " but does not have a correct description." + " Either " +
                    "apply an appropriate description, or put in Admin down."
                )
            else:
                if ("NN" or "UN") in "NN":
                    #print(p.description)
                    #print(type(p.description))
                #if ("NN" or "UN") in p.description:
                    list_report.append("PASS, port " + p.key + " is Administratively " + p.admin + " and configured " +
                        "to be either NNI or UNI."
                    )
                else:
                    list_report.append("FAIL, port " + p.key + " is Administratively " + p.admin + 
                        " but does not have a correct description." + " Either " +
                        "apply an appropriate description, or put in Admin down."
                    )
    '''

    # TEST, if it is Operationally up it must have a description
    for p in phyPorts:
        if p.oper == "up":
            #print("This is p.key")
            #print(p.key)
            #print("This is p.description")
            #print(p.description)
            if p.description is None:
                list_report.append("FAIL, port " + p.key + " is Operationally " + p.oper +
                    " but does not have a correct description." + " Either " +
                    "apply an appropriate description, or unplug the copper/fibre patch."
                )
            else:
                #if ("NN" or "UN") in p.description:
                #    #print(p.description)
                #    #print(type(p.description))
                #    list_report.append("PASS, port " + p.key + " is Operationally " + p.oper + " and configured " +
                #        "to be either NNI or UNI."
                #    )
                if "NN" in p.description:
                    list_report.append("PASS, port " + p.key + " is Operationally " + p.oper + " and configured " +
                        "to be NNI."
                    )
                elif "UN" in p.description:
                    list_report.append("PASS, port " + p.key + " is Operationally " + p.oper + " and configured " +
                        "to be UNI."
                    )
                else:
                    list_report.append("FAIL, port " + p.key + " is Operationally " + p.oper +
                        " but does not have a correct description." + " Either " +
                        "apply an appropriate description, or unplug the copper/fibre patch."
                    )


    # TEST, rx/tx errors
    for p in phyPortsErrors:
    # rx_err_xxx and tx_err_xxx are all "int"
        if p.rx_err_input == 0:
            list_report.append("PASS, port " + p.key + " does have " + str(p.rx_err_input) + " rx input errors.")
        else:
            list_report.append("FAIL, port " + p.key + " does have " + str(p.rx_err_input) + " rx input errors.")
        
        if p.rx_err_drops == 0:
            list_report.append("PASS, port " + p.key + " does have " + str(p.rx_err_drops) + " rx drop errors.")
        else:
            list_report.append("FAIL, port " + p.key + " does have " + str(p.rx_err_drops) + " rx drop errors.")
        
        if p.rx_err_frame == 0:
            list_report.append("PASS, port " + p.key + " does have " + str(p.rx_err_frame) + " rx frame errors.")
        else:
            list_report.append("FAIL, port " + p.key + " does have " + str(p.rx_err_frame) + " rx frame errors.")

        if p.rx_err_runts == 0:
            list_report.append("PASS, port " + p.key + " does have " + str(p.rx_err_runts) + " rx runt errors.")
        else:
            list_report.append("FAIL, port " + p.key + " does have " + str(p.rx_err_runts) + " rx runt errors.")
        
        if p.rx_err_discards == 0:
            list_report.append("PASS, port " + p.key + " does have " + str(p.rx_err_discards) + " rx discard errors.")
        else:
            list_report.append("FAIL, port " + p.key + " does have " + str(p.rx_err_discards) + " rx discard errors.")

        if p.rx_err_fifo == 0:
            list_report.append("PASS, port " + p.key + " does have " + str(p.rx_err_fifo) + " rx FIFO errors.")
        else:
            list_report.append("FAIL, port " + p.key + " does have " + str(p.rx_err_fifo) + " rx FIFO errors.")

        if p.rx_err_resource == 0:
            list_report.append("PASS, port " + p.key + " does have " + str(p.rx_err_resource) + " rx resource errors.")
        else:
            list_report.append("FAIL, port " + p.key + " does have " + str(p.rx_err_resource) + " rx resource errors.")

        
        if p.tx_err_drops == 0:
            list_report.append("PASS, port " + p.key + " does have " + str(p.tx_err_drops) + " tx drop errors.")
        else:
            list_report.append("FAIL, port " + p.key + " does have " + str(p.tx_err_drops) + " tx drop errors.")

        if p.tx_err_aged == 0:
            list_report.append("PASS, port " + p.key + " does have " + str(p.tx_err_aged) + " tx aged errors.")
        else:
            list_report.append("FAIL, port " + p.key + " does have " + str(p.tx_err_aged) + " tx aged errors.")

        if p.tx_err_fifo == 0:
            list_report.append("PASS, port " + p.key + " does have " + str(p.tx_err_fifo) + " tx FIFO errors.")
        else:
            list_report.append("FAIL, port " + p.key + " does have " + str(p.tx_err_fifo) + " tx FIFO errors.")

        if p.tx_err_mtu == 0:
            list_report.append("PASS, port " + p.key + " does have " + str(p.tx_err_mtu) + " tx MTU errors.")
        else:
            list_report.append("FAIL, port " + p.key + " does have " + str(p.tx_err_mtu) + " tx MTU errors.")

        if p.tx_err_resource == 0:
            list_report.append("PASS, port " + p.key + " does have " + str(p.tx_err_resource) + " tx resource errors.")
        else:
            list_report.append("FAIL, port " + p.key + " does have " + str(p.tx_err_resource) + " tx resource errors.")

    device.close()
    return list_report


'''
# mark
####  CONSTANTS  ####
fqdn = 'edge3-testlab.nn.hea.net'
nni_neighbors_expected = [ 'edge1-testlab', 'edge88-testlab' ]
local_username = 'heanet'
local_password = 'KqV7X98v!'

fqdn = 'dist1-lyit1.nn.hea.net'
#fqdn = 'dist1-lyit2.nn.hea.net'
fqdn = 'edge1-nuig-asng.nn.hea.net'
local_username = 'rancid'
local_password = '#pW5MV4G!q%3341sfsdFSS!@'
####  CONSTANTS  ####

import socket
address_ipv4 = (socket.gethostbyname(fqdn))
address_ipv6 = socket.getaddrinfo(fqdn, None, socket.AF_INET6)[0][4][0]

phyport_audit_report = audit_jnpr_phyport(address_ipv4, local_username, local_password)
phyport_audit_report.insert(0, "****  " + fqdn + "  ****" + "  ********  Physical Ports audit report, begin  ********")
phyport_audit_report.append("****  " + fqdn + "  ****" + "  ********  Physical Ports audit report, end  ********")
for i in phyport_audit_report:
    print(i)
'''

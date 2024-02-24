
def aux_jnpr_figure_chassis(address_ip, os_username, os_password):
    '''
    http://www.diveintopython3.net/xml.html
    https://docs.python.org/3.4/library/xml.etree.elementtree.html#finding-interesting-elements
    https://stackoverflow.com/questions/22135250/python-elementtree-find-element-by-its-childs-text-using-xpath
    '''

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


    from lxml import etree

    chassis_inventory = device.rpc.get_chassis_inventory()
    # If you want to see the output of chassis_inventory
    # https://stackoverflow.com/questions/22718101/pretty-print-option-in-tostring-not-working-in-lxml
    # print(etree.tostring(chassis_inventory, pretty_print=True, encoding='unicode'))
    # print(etree.tostring(chassis_inventory, pretty_print=True).decode())

    for element in chassis_inventory.findall('.//chassis'):
        chassis_description = element.find('description').text

    #chassis = chassis_inventory.find('.//chassis').tag
    #print(chassis)
    if chassis_description == 'ACX2200':
        function_outcome = "Chassis is an ACX2200"
    elif chassis_description == 'ACX5048':
        function_outcome = "Chassis is an ACX5048"
    elif chassis_description == 'MX40-T':
        function_outcome = "Chassis is an MX40-T"
    elif chassis_description == 'MX104':
        function_outcome = "Chassis is an MX104"
    elif chassis_description == 'MX240':
        function_outcome = "Chassis is an MX240"
    elif chassis_description == 'MX480':
        function_outcome = "Chassis is an MX480"
    elif chassis_description == 'MX960':
        function_outcome = "Chassis is an MX960"
    else:
        function_outcome = "Can't determinet the chassis description"

    return function_outcome


# mark
# To test this function, uncomment this block
####  CONSTANTS  ####
#fqdn = 'edge1-testlab.nn.hea.net'
#fqdn = 'edge2-testlab.nn.hea.net'
#fqdn = 'edge3-testlab.nn.hea.net'
#local_username = 'heanet'
#local_password = 'KqV7X98v!'

fqdn = 'edge4-testlab.nn.hea.net'
#fqdn = 'edge5-testlab.nn.hea.net'
local_username = 'heanet'
local_password = '$!3u$uxqDMTXzw9'

#fqdn = 'edge1-dcu-glasnevin.nn.hea.net'
#fqdn = 'edge1-dcu-spd2.nn.hea.net'
#fqdn = 'edge2-dcu.nn.hea.net'
#fqdn = 'dist1-lyit2.nn.hea.net'
#fqdn = 'rr1-pw.nn.hea.net'
#fqdn = 'core2-blanch.nn.hea.net'
#fqdn = 'core2-pw.nn.hea.net'
#local_username = 'rancid'
#local_password = '#pW5MV4G!q%3341sfsdFSS!@'
####  CONSTANTS  ####

import socket
address_ipv4 = (socket.gethostbyname(fqdn))
#address_ipv6 = socket.getaddrinfo(fqdn, None, socket.AF_INET6)[0][4][0]

audit_report = aux_jnpr_figure_chassis(address_ipv4, local_username, local_password)
print(audit_report)


'''
{master:0}
heanet@edge4-testlab> show chassis hardware | display xml | no-more
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/17.1R2/junos">
    <chassis-inventory xmlns="http://xml.juniper.net/junos/17.1R2/junos-chassis">
        <chassis junos:style="inventory">
            <name>Chassis</name>
            <serial-number>WB3716510241</serial-number>
            <description>ACX5048</description>
            <chassis-module>
                <name>Pseudo CB 0</name>
            </chassis-module>
            <chassis-module>
                <name>Routing Engine 0</name>
                <part-number>BUILTIN</part-number>
                <serial-number>BUILTIN</serial-number>
                <description>ACX5K Routing Engine</description>
                <clei-code>IPM9500DRB</clei-code>
                <model-number>ACX5048-AC</model-number>
            </chassis-module>
            <chassis-module>
                <name>FPC 0</name>
                <version>REV 05</version>
                <part-number>650-066414</part-number>
                <serial-number>WB3716510241</serial-number>
                <description>ACX5048</description>
                <clei-code>IPM9500DRB</clei-code>
                <model-number>ACX5048-AC</model-number>
                <chassis-sub-module>
                    <name>CPU</name>
                    <part-number>BUILTIN</part-number>
                    <serial-number>BUILTIN</serial-number>
                    <description>FPC CPU</description>
                </chassis-sub-module>
                <chassis-sub-module>
                    <name>PIC 0</name>
                    <part-number>BUILTIN</part-number>
                    <serial-number>BUILTIN</serial-number>
                    <description>48x10G-6x40G</description>
                    <clei-code>IPM9500DRB</clei-code>
                    <model-number>ACX5048-AC</model-number>
                    <chassis-sub-sub-module>
                        <name>Xcvr 3</name>
                        <version>REV 02</version>
                        <part-number>740-013111</part-number>
                        <serial-number>B371713</serial-number>
                        <description>SFP-T</description>
                    </chassis-sub-sub-module>
                    <chassis-sub-sub-module>
                        <name>Xcvr 47</name>
                        <part-number>NON-JNPR</part-number>
                        <serial-number>F786HU8</serial-number>
                        <description>SFP+-10G-LR</description>
                    </chassis-sub-sub-module>
                </chassis-sub-module>
            </chassis-module>
            <chassis-module>
                <name>Power Supply 0</name>
                <version>REV 04</version>
                <part-number>740-041741</part-number>
                <serial-number>1GA26450724</serial-number>
                <description>JPSU-650W-AC-AFO</description>
                <clei-code>CMUPABHBAB</clei-code>
                <model-number>JPSU-650W-AC-AFO</model-number>
            </chassis-module>
            <chassis-module>
                <name>Power Supply 1</name>
                <version>REV 04</version>
                <part-number>740-041741</part-number>
                <serial-number>1GA26450725</serial-number>
                <description>JPSU-650W-AC-AFO</description>
                <clei-code>CMUPABHBAB</clei-code>
                <model-number>JPSU-650W-AC-AFO</model-number>
            </chassis-module>
            <chassis-module>
                <name>Fan Tray 0</name>
                <description>ACX5K Fan Tray 0, Front to Back Airflow - AFO</description>
                <model-number>ACX5K-FAN</model-number>
            </chassis-module>
            <chassis-module>
                <name>Fan Tray 1</name>
                <description>ACX5K Fan Tray 1, Front to Back Airflow - AFO</description>
                <model-number>ACX5K-FAN</model-number>
            </chassis-module>
            <chassis-module>
                <name>Fan Tray 2</name>
                <description>ACX5K Fan Tray 2, Front to Back Airflow - AFO</description>
                <model-number>ACX5K-FAN</model-number>
            </chassis-module>
            <chassis-module>
                <name>Fan Tray 3</name>
                <description>ACX5K Fan Tray 3, Front to Back Airflow - AFO</description>
                <model-number>ACX5K-FAN</model-number>
            </chassis-module>
            <chassis-module>
                <name>Fan Tray 4</name>
                <description>ACX5K Fan Tray 4, Front to Back Airflow - AFO</description>
                <model-number>ACX5K-FAN</model-number>
            </chassis-module>
        </chassis>
    </chassis-inventory>
    <cli>
        <banner>{master:0}</banner>
    </cli>
</rpc-reply>

{master:0}
heanet@edge4-testlab>
'''

'''
python 3.4 at least
needs
junos-eznc
'''

'''
###############################################################################
#  CONSTANTS  #
fqdn = 'edge3-testlab.nn.hea.net'
loopback_ipv4 = '87.44.48.23'   # edge3-testlab.nn.hea.net
loopback_ipv6 = '2001:0770:0200::23'
neighbors_expected = ['edge1-testlab', 'edge88-testlab']
local_username = 'heanet'
local_password = 'KqV7X98v!'

fqdn = 'edge1-dcu-glasnevin.nn.hea.net'
loopback_ipv4 = '87.44.48.15'
loopback_ipv6 = '2001:0770:0200::15'

fqdn = 'dist1-wat-car2.nn.hea.net'
loopback_ipv4 = '87.44.48.55'
loopback_ipv6 = '2001:0770:0200::55'

fqdn = 'edge2-dcu.nn.hea.net'
loopback_ipv4 = '87.44.48.12'
loopback_ipv6 = '2001:770:200::12'

#fqdn = 'core1-blanch.nn.hea.net'
#loopback_ipv4 = '87.44.48.36'
#loopback_ipv6 = '2001:770:200::36

local_username = 'rancid'
local_password = '#pW5MV4G!q%3341sfsdFSS!@'
###############################################################################
'''

def audit_transceivers_juniper(address_ipv4, os_username, os_password):
    """ Audit Juniper PIC transceivers. Interrogates a Juniper device for 

    transceivers installed and compares those against a catalogue of 
    transceivers. 

    Args:
        address_ipv4 (str): IPv4 or IPv6 address.
        os_username (str): username in JUNOS with at least read access.
        os_password (str): password for the JUNOS username above.

    Returns:
        list: list with one PASS/FAIL for each transceiver.

    Requires:
        Python, >= 3.4
        junos-eznc, >= 2.1.2

    Version:
        0.4

    To do:
        xxx
    """

    # Code based on:
    # https://groups.google.com/forum/#!topic/junos-python-ez/wuvHw_J7gBE
    from jnpr.junos import Device
    from jnpr.junos.factory.factory_loader import FactoryLoader
    from jnpr.junos.op.fpc import FpcHwTable
    import sys
    import yaml

    # initialize an empty list, this is what the function will return
    #header = device.facts['hostname'] + ", transceivers audit report"
    import socket
    #print(socket.gethostbyaddr(address_ipv4)[0])
    #header = str(address_ipv4) + ", transceivers audit report"
    #header = socket.gethostbyaddr(address_ipv4)[0] + ", transceivers audit report"
    #list_report = [header]
    list_report = []

    # Connect to device.
    device = Device(host=address_ipv4, user=os_username, password=os_password)
    try:
        device.open(gather_facts=False)
    except Exception as err:
        print("Unable to connect to host:", err)
        sys.exit(1)

    # Yaml table
    yaml_data = \
    """
---
TransceiversTable:
  rpc: get-pic-detail
  args_key: fpc-slot
  item: fpc/pic-detail/port-information/port
  key: port-number
  view: TransceiversView

TransceiversView:
  fields:
    port_no: port-number
    cable_type: cable-type
    fibre_type: fiber-mode
    vendor_part_number: sfp-vendor-pno
    vendor_name: sfp-vendor-name
    wavelenght: wavelength
   """

    globals().update(FactoryLoader().load(yaml.load(yaml_data)))
    transceivers_seen = TransceiversTable(device)

    # dictionary of dictionaries
    # Flexoptics part numbers, explanation in
    # https://www.flexoptix.net/en/flexoptix-part-numbers/
    transceivers_catalogue = {
        'FIM3850': { 'manufacturer': 'JUNIPER-FUJITSU', 'part_number': 'FIM38500/222',
            'form_factor': 'CFP', 'physical_layer': 'LH',
            'description': '100G CFP LR4',
            'correct_encode_string': '100G LH'
        },
        'FTLF131': { 'manufacturer': 'FINISAR', 'part_number': 'FTLF1318P2BCL-CS',
            'form_factor': 'SFP', 'physical_layer': 'LX',
            'description': '1G SFP LX',
            'correct_encode_string': 'SFP-1GE-LX'
        },
        'FTLC118': { 'manufacturer': 'FINISAR', 'part_number': 'FTLC1183RDNL-J5',
            'form_factor': 'CFP', 'physical_layer': 'LR',
            'description': '100G CFP LR4',
            'correct_encode_string': '100G LR'
        },
        'P139610': {'form_factor': 'SFP+', 'physical_layer': 'LR',
            'description': '10G SFP+ LR',
            'correct_encode_string': 'SFP-10GE-LR'
        },
        'P159680': { 'manufacturer': 'FLEXOPTICS', 'part_number': 'P.1596.80',
            'form_factor': 'SFP+', 'physical_layer': 'ZR',
            'description': '10G SFP+ ZR',
            'correct_encode_string': 'SFP-10GE-ZR'
        },
        'P169610': {'form_factor': 'SFP+', 'physical_layer': 'LR',
            'description': '10G SFP+ CWDM LR',
            'correct_encode_string': 'SFP-10G-LR'
            },
        'P169623': {'form_factor': 'SFP+', 'physical_layer': 'ZR',
            'description': '10G SFP+ DWDM ZR',
            'correct_encode_string': 'SFP-10G-ZR'
            },
        'S131210': {'form_factor': 'SFP', 'part_number': 'S.1312.10.x',
            'physical_layer': 'LX',
            'description': '1G SFP LX',
            'correct_encode_string': 'SFP-1GE-LX'
            },
        'S151280': { 'manufacturer': 'FLEXOPTICS', 'part_number': 'S.1512.80.D',
            'form_factor': 'SFP', 'physical_layer': 'ZX',
            'description': '1G SFP ZX',
            'correct_encode_string': 'SFP-1GE-ZX xxx'
        },
        'S161225': {'form_factor': 'SFP', 'part_number': 'S.1612.25.xy',
            'physical_layer': 'ZX',
            'description': '1G SFP CWDM ZX',
            'correct_encode_string': 'SFP-1GE-ZX xxx'
        },
        'S161237': {'form_factor': 'SFP', 'physical_layer': 'ZX+',
            'description': '1G SFP CWDM ZX+',
            'correct_encode_string': 'SFP-1G-ZX+ xxx'
            },
        'S851202': { 'manufacturer': 'FLEXOPTICS', 'part_number': 'S.8512.02.D',
            'form_factor': 'SFP', 'physical_layer': 'SX',
            'description': '1G SFP SX',
            'correct_encode_string': 'SFP-1GE-SX'
        },
        'TC1202A': {'form_factor': 'SFP', 'physical_layer': 'T',
            'description': '1000BASE-T COPPER SFP',
            'correct_encode_string': 'SFP-1GE-T'
            },
        'X139610': {'form_factor': 'XFP', 'physical_layer': 'LR',
            'description': '10G XFP LR',
            'correct_encode_string': 'XFP-10G-L-OC192-SR1'
            },
        'X169623': {'form_factor': 'XFP', 'physical_layer': 'ZR',
            'description': '10G XFP CWDM ZR',
            'correct_encode_string': 'XFP-10GE-ZR'
            },
    }

    '''
    # initialize an empty list, this is what the function will return
    #header = device.facts['hostname'] + ", transceivers audit report"
    import socket
    #print(socket.gethostbyaddr(address_ipv4)[0])
    #header = str(address_ipv4) + ", transceivers audit report"
    header = socket.gethostbyaddr(address_ipv4)[0] + ", transceivers audit report"
    list_report = [header]
    '''

    # Go get them tiger!!
    fpcs = FpcHwTable(device).get()
    for fpc in fpcs:
        # Get the slot number of the FPC. Because fpc.key output is something
        # like: "FPC 0", we need to strip the last character.
        fpc_slot_number = str(fpc.key[-1:])

        if device.facts['model'] is None:
            if "ACX5K" in device.facts['RE0']['model']:
                number_of_pics = range(0, 3)
        else:
            number_of_pics = range(0, 4)

        # Each FPC has 4 PIC
        #for pic_number in range(0, 4):
        for pic_number in number_of_pics:
            transceiver_seen = transceivers_seen.get(fpc_slot_number,
                pic_slot=str(pic_number)
            )
            for item in transceiver_seen:
                # normalize = remove the "dots" and remove the last two digits
                # of what the CLI output
                #print("SEEN")
                #print(item.vendor_part_number)

                normalized_part_number_seen = item.vendor_part_number[:9].replace('.', '')
                normalized_part_number_seen = item.vendor_part_number.replace('.', '')[:7]
                #print("NORMALIZED")
                #print(normalized_part_number_seen)

                # get all the transceivers part numbers in a list so that
                # we can compare with the CLI output.
                list_of_transceivers_catalogue = list(
                    transceivers_catalogue.keys()
                )
                #print("list_of_transceivers_catalogue")
                #print(list_of_transceivers_catalogue)

                if normalized_part_number_seen in list_of_transceivers_catalogue:
                    if transceivers_catalogue[normalized_part_number_seen]['physical_layer'] in item.cable_type:
                        list_report.append("PASS: transceiver in FPC slot " +
                            str(fpc_slot_number) + " and PIC slot " +
                            str(pic_number) + " is correctly encoded."
                        )
                    else:
                        list_report.append("FAIL: transceiver in FPC slot " +
                            str(fpc_slot_number) + " and PIC slot " +
                            str(pic_number) + " is incorrectly encoded."
                        )
                    list_report.append("The transceiver has part number: " +
                        item.vendor_part_number + ". The correct encoding is: " +
                        transceivers_catalogue[normalized_part_number_seen]['correct_encode_string'] +
                        ". It has been encoded as: " + item.cable_type
                    )

                if normalized_part_number_seen not in list_of_transceivers_catalogue:
                    # If the router shows a transceiver of which we do not
                    # know anything about. That we do not have in the catalogue
                    list_report.append("WARNING: the trasceiver with part number " + str(item.vendor_part_number) +
                        " is not in the catalogue"
                    )

    #list_report.append("\n")
    device.close()
    return list_report


'''
import socket

number_of_pass = 0
number_of_fail = 0

# get file object f
f = open('rman_pes.txt', 'r')

# https://docs.python.org/3/tutorial/inputoutput.html
for line in f:
    fqdn = line.split(':')[0]
    #print(fqdn)
    address_ipv4 = (socket.gethostbyname(fqdn))
    #print(address_ipv4)
    report = audit_transceivers_juniper(address_ipv4, local_username, local_password)
    for i in report:
        print(i)
        if "PASS" in i:
            number_of_pass = number_of_pass + 1
        if "FAIL" in i:
            number_of_fail = number_of_fail + 1

print("Number of PASS: " + str(number_of_pass))
print("Number of FAIL: " + str(number_of_fail))
print("PASS is: " + str(round(number_of_pass/(number_of_pass+number_of_fail)*100)) + "%")
print("FAIL is: " + str(round(number_of_fail/(number_of_pass+number_of_fail)*100)) + "%")
'''

'''
pes_named = ['edge1-dcu.nn.hea.net', 'edge2-dcu.nn.hea.net']
for pe in pes_named:
    print(socket.gethostbyname(pe))

pes = ['87.44.48.7', '87.44.48.8', '87.44.48.12', '87.44.48.14', '87.44.48.52', '87.44.48.53', '87.44.48.54', '87.44.48.55']
#pes = ['87.44.48.12']
#pes = ['87.44.48.52', '87.44.48.53', '87.44.48.54', '87.44.48.55']
number_of_pass = 0
number_of_fail = 0
for pe in pes:
    report = audit_transceivers_juniper(pe, local_username, local_password)
    for i in report:
        print(i)
        if "PASS" in i:
            number_of_pass = number_of_pass + 1
        if "FAIL" in i:
            number_of_fail = number_of_fail + 1

print("Number of PASS: " + str(number_of_pass))
print("Number of FAIL: " + str(number_of_fail))
print("PASS is: " + str(round(number_of_pass/(number_of_pass+number_of_fail)*100)) + "%")
print("FAIL is: " + str(round(number_of_fail/(number_of_pass+number_of_fail)*100)) + "%")
'''

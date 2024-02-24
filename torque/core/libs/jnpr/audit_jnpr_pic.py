
def audit_jnpr_transceiver(address_ipv4, os_username, os_password):
    ''' Audit Juniper PIC transceivers. Interrogates a Juniper device for 
    transceivers installed and compares those against a catalogue of 
    transceivers. 

    Args:
        address_ipv4 (str): IPv4 or IPv6 address.
        os_username (str): username in JUNOS with at least read access.
        os_password (str): password for the JUNOS username above.

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

    # Code based on:
    # https://groups.google.com/forum/#!topic/junos-python-ez/wuvHw_J7gBE
    ''' Import junos-eznc base function and open Netconf session. '''
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
    #device = Device(host=address_ipv4, user=os_username, password=os_password)
    try:
        Device.auto_probe = 5
        device = Device(
            host=address_ipv4,
            user=os_username,
            password=os_password,
            gather_facts=False)
        device.open()
    except Exception as err:
        list_report.append("WARNING, the following error has happened: " + str(err))
        return list_report
        #print("Unable to connect to host:", err)
        #sys.exit(1)

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
        # ok
        'FIM3850': { 'manufacturer': 'JUNIPER-FUJITSU', 'part_number': 'FIM38500/222',
            'form_factor': 'CFP', 'physical_layer': 'LH',
            'description': '100G CFP LR4',
            'correct_encode_string': '100G LH'
        },
        # ok
        'FTLF131': { 'manufacturer': 'FINISAR', 'part_number': 'FTLF1318P2BCL-CS',
            'form_factor': 'SFP', 'physical_layer': 'LX',
            'description': '1G SFP LX',
            'correct_encode_string': 'SFP-1GE-LX'
        },
        # ok
        'FTLC118': { 'manufacturer': 'FINISAR', 'part_number': 'FTLC1183RDNL-J5',
            'form_factor': 'CFP', 'physical_layer': 'LR',
            'description': '100G CFP LR4',
            'correct_encode_string': '100G LR'
        },
        # Finisar 1G SX Fibre Channel, https://www.cnet.com/products/finisar-ftrj-8519-7d-sfp-mini-gbic-transceiver-module-fibre-channel/specs/
        'FTRJ85197DCSC': { 'manufacturer': 'FINISAR', 'part_number': 'FTRJ-8519-7D-CSC',
            'form_factor': 'SFP', 'physical_layer': 'SX',
            'description': '1G SFP SX',
            'correct_encode_string': 'SFP-1GE-SX'
        },
        # Finisar 1G SX
        'FTRJ8519P1BNLC5': { 'manufacturer': 'FINISAR', 'part_number': 'FTRJ8519P1BNL-C5',
            'form_factor': 'SFP', 'physical_layer': 'SX',
            'description': '1G SFP SX',
            'correct_encode_string': 'SFP-1GE-SX'
        },
        # Finisar 1G SX
        'FTRJ8519P1BNLC6': { 'manufacturer': 'FINISAR', 'part_number': 'FTRJ8519P1BNL-C6',
            'form_factor': 'SFP', 'physical_layer': 'SX',
            'description': '1G SFP SX',
            'correct_encode_string': 'SFP-1GE-SX'
        },
        # ok
        'P139610': {'form_factor': 'SFP+', 'physical_layer': 'LR',
            'description': '10G SFP+ LR',
            'correct_encode_string': 'SFP-10GE-LR'
        },
        'P139640': {'form_factor': 'SFP+', 'physical_layer': 'ER',
            'description': '10G SFP+ ER',
            'correct_encode_string': 'SFPP-10GE-ER'
        },
        # pending to have correct coding string
        'P159680': { 'manufacturer': 'FLEXOPTICS', 'part_number': 'P.1596.80',
            'form_factor': 'SFP+', 'physical_layer': 'ZR',
            'description': '10G SFP+ ZR',
            'correct_encode_string': 'SFP-10GE-ZR'
        },
        # pending to have correct coding string
        'P169610': {'form_factor': 'SFP+', 'physical_layer': 'LR',
            'description': '10G SFP+ CWDM LR',
            'correct_encode_string': 'SFP-10G-LR'
        },
        # ok. Other alternatives are SFP+-DWDM-23dB-C31 or SFP-DWDM-28dB-C31
        'P169623': {'form_factor': 'SFP+', 'physical_layer': 'ZR',
            'description': '10G SFP+ DWDM ZR',
            'correct_encode_string': 'SFP-10G-ZR'
        },
        'P169625': {'form_factor': 'SFP+', 'physical_layer': 'ZR+',
            'description': '10G SFP+ DWDM ZR+',
            'correct_encode_string': 'SFP-10G-ZR+'
        },
        'P859602': {'form_factor': 'SFP+', 'physical_layer': 'SR',
            'description': '10G SFP+ SR',
            'correct_encode_string': 'SFPP-10GE-SR'
        },
        # ok
        'S131210': {'form_factor': 'SFP', 'part_number': 'S.1312.10.x',
            'physical_layer': 'LX',
            'description': '1G SFP LX',
            'correct_encode_string': 'SFP-1GE-LX'
        },
        # pending to have correct coding string
        'S151280': { 'manufacturer': 'FLEXOPTICS', 'part_number': 'S.1512.80.D',
            'form_factor': 'SFP', 'physical_layer': 'ZX',
            'description': '1G SFP ZX',
            'correct_encode_string': 'SFP-1GE-ZX xxx'
        },
        # pending to have correct coding string. Options EX-SFP-GE80KCW1590 or SFP-1GE-LH or SFP-CWDM-25dB-1590
        'S161225': {'form_factor': 'SFP', 'part_number': 'S.1612.25.xy',
            'physical_layer': 'ZX',
            'description': '1G SFP CWDM ZX',
            'correct_encode_string': 'SFP-1GE-ZX xxx'
        },
        # pending to have correct coding string
        'S161237': {'form_factor': 'SFP', 'physical_layer': 'ZX+',
            'description': '1G SFP CWDM ZX+',
            'correct_encode_string': 'SFP-1G-ZX+ xxx'
        },
        # pending to have correct coding string
        'S851202': { 'manufacturer': 'FLEXOPTICS', 'part_number': 'S.8512.02.D',
            'form_factor': 'SFP', 'physical_layer': 'SX',
            'description': '1G SFP SX',
            'correct_encode_string': 'SFP-1GE-SX'
        },
        # ok
        'TC1202A': {'form_factor': 'SFP', 'physical_layer': 'T',
            'description': '1000BASE-T COPPER SFP',
            'correct_encode_string': 'SFP-1GE-T'
        },
        # ok
        'X139610': {'form_factor': 'XFP', 'physical_layer': 'LR',
            'description': '10G XFP LR',
            'correct_encode_string': 'EX-XFP-10GE-LR'
        },
        # pending to have correct coding string
        'X169623': {'form_factor': 'XFP', 'physical_layer': 'ZR',
            'description': '10G XFP CWDM ZR',
            'correct_encode_string': 'XFP-10GE-ZR'
        },
    }


    # Go get them tiger!!
    fpcs = FpcHwTable(device).get()
    for fpc in fpcs:
        # Get the slot number of the FPC. Because fpc.key output is something
        # like: "FPC 0", we need to strip the last character.
        fpc_slot_number = str(fpc.key[-1:])

        #if device.facts['model'] is None:
        #    if "ACX5K" in device.facts['RE0']['model']:
        #        number_of_pics = range(0, 3)
        #else:
        #    number_of_pics = range(0, 4)

        ''' Find out what type of chassis we are dealing with '''
        from lxml import etree
        chassis_inventory = device.rpc.get_chassis_inventory()
        for element in chassis_inventory.findall('.//chassis'):
            chassis_description = element.find('description').text

        if (chassis_description == 'ACX5048'):
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

                # HAVE TO FIX FINISAR, slice the first 15 characters
                #normalized_part_number_seen = item.vendor_part_number[:15].replace('-', '')

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
                            str(pic_number) + " is correctly encoded. " + "The transceiver has part number: " +
                            item.vendor_part_number + ". The correct encoding is: " +
                            transceivers_catalogue[normalized_part_number_seen]['correct_encode_string'] +
                            ". It has been encoded as: " + item.cable_type
                        )
                    else:
                        #list_report.append("FAIL: transceiver in FPC slot " +
                        list_report.append("WARNING: transceiver in FPC slot " +
                            str(fpc_slot_number) + " and PIC slot " +
                            str(pic_number) + " is incorrectly encoded. " + "The transceiver has part number: " +
                            item.vendor_part_number + ". The correct encoding is: " +
                            transceivers_catalogue[normalized_part_number_seen]['correct_encode_string'] +
                            ". It has been encoded as: " + item.cable_type
                        )
                    '''
                    list_report.append("The transceiver has part number: " +
                        item.vendor_part_number + ". The correct encoding is: " +
                        transceivers_catalogue[normalized_part_number_seen]['correct_encode_string'] +
                        ". It has been encoded as: " + item.cable_type
                    )
                    '''

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
#fqdn = 'dist1-lyit2.nn.hea.net'
#fqdn = 'rr1-pw.nn.hea.net'
#fqdn = 'core2-blanch.nn.hea.net'
#fqdn = 'core2-pw.nn.hea.net'
#list_of_fqdn = [ 'edge1-dcu-glasnevin.nn.hea.net', 'edge1-dcu-spd2.nn.hea.net', 'dist1-lyit2.nn.hea.net', 'rr1-pw.nn.hea.net', 'core2-  blanch.nn.hea.net', 'core2-pw.nn.hea.net']
#local_username = 'rancid'
#local_password = '#pW5MV4G!q%3341sfsdFSS!@'
####  CONSTANTS  ####

import socket
try:
    address_ip = (socket.gethostbyname(fqdn))
except Exception as err:
    print(str(err))

audit_report = audit_jnpr_transceiver(address_ip, local_username, local_password)
for i in audit_report:
    print(i)
'''

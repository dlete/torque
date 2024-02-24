
def audit_jnpr_intopticdiag(address_ip, os_username, os_password):
    '''Return list of test results for Interface Optical Diagnostics.

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
        PyYAML 3.12

    To-do:
        Add error handling. We are not checking what to do if we can't connect
        to the Device
        Add test for 100G interfaces. At the moment the script does not capture them.
    '''


    ''' Initialize, empty, the list that the function will return. '''
    list_report = []

    ''' Import junos-eznc base function and open Netconf session. '''
    from jnpr.junos import Device
    try:
        Device.auto_probe = 5
        device = Device(host=address_ip, user=os_username, password=os_password)
        device.open(gather_facts=False)
    except Exception as err:
        list_report.append("WARNING, the following error has happened: " + str(err))
        return list_report

    ''' We are going to build our own junos-eznc table. '''
    from jnpr.junos.factory.factory_loader import FactoryLoader
    import yaml
    yaml_data = \
    """
---
MyPhyPortDiagTable:
  rpc: get-interface-optics-diagnostics-information
  args:
    interface_name: '[efgx][et]-*'
  args_key: interface_name
  item: physical-interface
  view: MyPhyPortDiagView

MyPhyPortDiagView:
  groups:
    diag: optics-diagnostics

  # fields that are part of groups are called
  # "fields_<group-name>"

  fields_diag:
    rx_optic_power: laser-rx-optical-power-dbm 
    laser_output_power_dbm: laser-output-power-dbm
    laser_rx_optical_power_dbm: laser-rx-optical-power-dbm
    laser_rx_optical_power_dbm: laser-rx-optical-power

    rx_optic_power_avg: rx-signal-avg-optical-power-dbm
    rx_high_alarm: laser-rx-power-high-alarm-threshold-dbm
    rx_low_alarm: laser-rx-power-low-alarm-threshold-dbm
    rx_high_warn: laser-rx-power-high-warn-threshold-dbm
    rx_low_warn: laser-rx-power-low-warn-threshold-dbm

    tx_optic_power : laser-output-power-dbm
    tx_high_alarm: laser-tx-power-high-alarm-threshold-dbm
    tx_low_alarm: laser-tx-power-low-alarm-threshold-dbm
    tx_high_warn: laser-tx-power-high-warn-threshold-dbm
    tx_low_warn: laser-tx-power-low-warn-threshold-dbm

    module_temperature: module-temperature
    temperature_high_alarm: module-temperature-high-alarm-threshold
    temperature_low_alarm: module-temperature-low-alarm-threshold
    temperature_high_warn: module-temperature-high-warn-threshold
    temperature_low_warn: module-temperature-low-warn-threshold

    module_voltage : module-voltage
    voltage_high_alarm: module-voltage-high-alarm-threshold
    voltage_low_alarm: module-voltage-low-alarm-threshold
    voltage_high_warn: module-voltage-high-warn-threshold
    voltage_low_warn: module-voltage-low-warn-threshold

    laser-bias: laser-bias-current
    laser-bias_high_alarm: laser-bias-current-high-alarm-threshold
    laser-bias_low_alarm: laser-bias-current-low-alarm-threshold
    laser-bias_high_warn: laser-bias-current-high-warn-threshold
    laser-bias_low_warn: laser-bias-current-low-warn-threshold
    """

    ''' Retrieve data from the Ne '''
    globals().update(FactoryLoader().load(yaml.load(yaml_data)))
    ports = MyPhyPortDiagTable(device).get()

    '''
    for p in ports:
        print("p.key")
        print(p.key)
        print("laser_output_power_dbm")
        print(p.laser_output_power_dbm)
        print("tx_optic_power")
        print(p.tx_optic_power)
        print("rx_optic_power")
        print(p.rx_optic_power)
        print(type(p.rx_optic_power))
        print("port.rx_optic_power_avg")
        print(p.rx_optic_power_avg)
        print(type(p.rx_optic_power_avg))
    '''

    # How many transceivers are plugged in the Ne. It is an (int)
    number_of_transceivers = ports.__len__()
    # If there are no transceives, give back a PASS message to the user and 
    # terminate and exit the function.
    if number_of_transceivers == 0:
        list_report.append("PASS, there are no transceivers in this device. " +
            "No point measuring optical power values here")
        return list_report


    # If we are here, we have transceivers. Now, beware, if the transceiver is
    # not connected, it will report a rx_optic_power of "None" and it will be
    # an object <class 'NoneType'>.
    for port in ports:
        #print('follows port.rx_optic_power')
        #print(port.rx_optic_power)
        if port.rx_optic_power is not None:
            if 'Inf' in port.rx_optic_power:
                #print('port.rx_optic_power does contain the keyword Inf')
                #rx_power = 0
                list_report.append("WARNING, there is a transceiver plugged in: " +
                    port.key + " but nothing is connected to it.")
                continue
            else:
                rx_power = port.rx_optic_power      # (str)
        elif port.rx_optic_power_avg is not None:
            if 'Inf' in port.rx_optic_power_avg:
                #print('port.rx_optic_power_avg does contain the keyword Inf')
                #rx_power = 0
                list_report.append("WARNING, there is a transceiver plugged in: " +
                    port.key + " but nothing is connected to it.")
                continue
            else:
                rx_power = port.rx_optic_power_avg  # (str)
        else:
            list_report.append("WARNING, can't determine what type of " +
                "transceiver is plugged in " + port.key + ". Most probably " +
                "is a 100G (tunable DWDM or LR4). Please do this check manually.")
            continue
            

		# do all the if rx - threshold is > 3 then to this or that
        # How many dBm we want between rx value and threshold?
        guard = int(3)                                      # (int)

        # TEST, rx optical power (dBm) is at least "guard" dBm from the High Warning
        #print(port.rx_high_warn)
        #print(float(port.rx_high_warn))
        #print(type(port.rx_high_warn))
        #print('follows: rx_power')
        #print(rx_power)
        #print('follows: type(rx_power)')
        #print(type(rx_power))
        #print(float(rx_power))
        #if 'Inf' in rx_power:
        #    print('ALERTA')
        #else:
        #    print('ALL FINE')
        delta_high = float(port.rx_high_warn) - float(rx_power)      # (float)
        if (delta_high) > guard:
            list_report.append("PASS, " + port.key + " transceiver rx power is " + str(rx_power) + " dBm and the " +
                "High Warning threshold is " + str(port.rx_high_warn) + " dBm. There are " +
                str(round(delta_high, 2)) + " dBm between them, that is more than " + 
                str(guard) + " dBm.")
        else:
            list_report.append("FAIL, " + port.key + " transceiver rx power is " + str(rx_power) + " dBm and the " +
                "High Warning threshold is " + str(port.rx_high_warn) + " dBm. There are " +
                str(round(delta_high, 2)) + " dBm between them, that is less than " +
                str(guard) + " dBm.")
    
        # TEST, rx optical power (dBm) is at least "guard" dBm from the Low Warning
        delta_low = float(rx_power) - float(port.rx_low_warn)        # (float)
        if (delta_low) > guard:
            list_report.append("PASS, " + port.key + " transceiver rx power is " + str(rx_power) + " dBm and the " +
                "Low Warning threshold is " + str(port.rx_low_warn) + " dBm. There are " +
                str(round(delta_low, 2)) + " dBm between them, that is more than " +
                str(guard) + " dBm.")
        else:
            list_report.append("FAIL, " + port.key + " transceiver rx power is " + str(rx_power) + " dBm and the " +
                "Low Warning threshold is " + str(port.rx_low_warn) + " dBm. There are " +
                str(round(delta_low, 2)) + " dBm between them, that is less than " +
                str(guard) + " dBm.")


        tx_warning_range = float(port.tx_high_warn) - float(port.tx_low_warn)     # (float)
        guard = tx_warning_range * 0.1                              # (float)

        # TEST, tx optical power (dBm) is at least "guard" dBm from the High Warning
        delta_high = float(port.tx_high_warn) - float(port.tx_optic_power)
        if delta_high > guard:
            list_report.append("PASS, " + port.key + " transceiver tx power is " + str(port.tx_optic_power) + " dBm and the " +
                "High Warning threshold is " + str(port.tx_high_warn) + " dBm. There are " +
                str(round(delta_high, 2)) + " dBm between them, that is more than " +
                str(round(guard, 2)) + " dBm.")
        else:
            list_report.append("FAIL, " + port.key + " transceiver tx power is " + str(port.tx_optic_power) + " dBm and the " +
                "High Warning threshold is " + str(port.tx_high_warn) + " dBm. There are " +
                str(round(delta_high, 2)) + " dBm between them, that is less than " +
                str(round(guard, 2)) + " dBm.")


        # TEST, tx optical power (dBm) is at least "guard" dBm from the Low Warning
        delta_low = float(port.tx_optic_power) - float(port.tx_low_warn)
        if delta_high > guard:
            list_report.append("PASS, " + port.key + " transceiver tx power is " + port.tx_optic_power + " dBm and the " +
                "Low Warning threshold is " + port.tx_low_warn + " dBm. There are " +
                str(round(delta_low, 2)) + " dBm between them, that is more than " +
                str(round(guard, 2)) + " dBm.")
        else:
            list_report.append("FAIL, " + port.key + " transceiver tx power is " + port.tx_optic_power + " dBm and the " +
                "Low Warning threshold is " + port.tx_low_warn + " dBm. There are " +
                str(round(delta_low, 2)) + " dBm between them, that is less than " +
                str(round(guard, 2)) + " dBm.")


        #print(port.temperature_high_warn.split(' ')[0])
        #print(port.temperature_low_warn.split(' ')[0])
        temperature_warning_range = int(port.temperature_high_warn.split(' ')[0]) - int(port.temperature_low_warn.split(' ')[0])
        guard = temperature_warning_range * 0.1     # (int) 
        #print(guard)
        #print(port.temperature_high_warn)
        #print(port.module_temperature)
        
        # TEST, module_temperature is at least "guard" from the High Warning
        delta_high = int(port.temperature_high_warn.split(' ')[0]) - int(port.module_temperature.split(' ')[0])
        #print(delta_high)
        if (delta_high) > guard:
            list_report.append("PASS, " + port.key + " transceiver temperature is " + port.module_temperature.split(' ')[0] + " Celsius and the " +
                "High Warning threshold is " + port.temperature_high_warn.split(' ')[0] + " Celsius. There are " +
                str(delta_high) + " Celsius between them, that is more than the " +
                str(round(guard, 2)) + " Celsius required.")
        else:
            list_report.append("FAIL, " + port.key + " transceiver temperature is " + port.module_temperature.split(' ')[0] + " Celsius and the " +
                "High Warning threshold is " + port.temperature_high_warn.split(' ')[0] + " Celsius. There are " +
                str(delta_high) + " Celsius between them, that is less than the " +
                str(round(guard, 2)) + " Celsius required.")


        # TEST, module_temperature is at least "guard" from the Low Warning
        delta_low = int(port.module_temperature.split(' ')[0]) - int(port.temperature_low_warn.split(' ')[0])
        if (delta_low) > guard:
            list_report.append("PASS, " + port.key + " transceiver temperature is " + port.module_temperature.split(' ')[0] + " Celsius and the " +
                "Low Warning threshold is " + port.temperature_low_warn.split(' ')[0] + " Celsius. There are " +
                str(delta_low) + " Celsius between them, that is more than the " +
                str(round(guard, 2)) + " Celsius required.")
        else:
            list_report.append("FAIL, " + port.key + " transceiver temperature is " + port.module_temperature.split(' ')[0] + " Celsius and the " +
                "Low Warning threshold is " + port.temperature_low_warn.split(' ')[0] + " Celsius. There are " +
                str(delta_low) + " Celsius between them, that is less than the " +
                str(round(guard, 2)) + " Celsius required.")

    device.close()
    return list_report


'''
# mark
####  CONSTANTS  ####
fqdn = 'edge1-testlab.nn.hea.net'
fqdn = 'edge2-testlab.nn.hea.net'
fqdn = 'edge3-testlab.nn.hea.net'
os_username = 'heanet'
os_password = 'KqV7X98v!'
#nni_neighbors_expected = [ 'edge1-testlab', 'edge88-testlab' ]
#print(nni_neighbors_expected)
#ibgp_ipv4_peers_expected = ['87.44.48.5', '87.44.48.6']
#print(ibgp_ipv4_peers_expected)
#ibgp_ipv6_peers_expected = ['2001:770:200::5', '2001:770:200::6']
#print(ibgp_ipv6_peers_expected)
#ibgp_peers_expected = ['87.44.48.5', '87.44.48.6', '2001:770:200::5', '2001:770:200::6']

#fqdn = 'edge1-dcu-glasnevin.nn.hea.net'
#fqdn = 'dist1-itb.nn.hea.net'
#fqdn = 'edge2-dcu.nn.hea.net'
#fqdn = 'core2-dcu.nn.hea.net'
#fqdn = 'core2-cwt.nn.hea.net'
fqdn = 'core1-blanch.nn.hea.net'
#fqdn = 'dist1-wat-car2.nn.hea.net'
#fqdn = 'edge1-tcd-lofar.nn.hea.net'
os_username = 'rancid'
os_password = '#pW5MV4G!q%3341sfsdFSS!@'
####  CONSTANTS  ####

import socket
address_ipv4 = (socket.gethostbyname(fqdn))
#address_ipv6 = socket.getaddrinfo(fqdn, None, socket.AF_INET6)[0][4][0]
#print(address_ipv6)
blah = audit_jnpr_intopticdiag(address_ipv4, os_username, os_password)
for i in blah:
    print(i)
'''

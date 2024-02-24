
def audit_jnpr_isis(address_ipv4, os_username, os_password, isis_settings):
    '''
    TO DO:
        - change format of outcome to (FAIL/PASS is the first keyword):
            [FAIL|PASS], IS-IS <test_type>, expected <what_was_expected>, actual <what_has_been_seen>
        - present circuit-type as P2P instead of 2
        - authentication is enabled
        - BFD is enabled
        - metric is as it should (ref_bandwidth/nominal_bandwidth)
        - neighbors seen are neighbors expected
        - no ohter SPF than database expiry. 
        - size of database is as expected. 
        - all circuits are p2p
        - come up with a way to work together with Garwin.
        - improve speed. I suspect is related to retrieving in json. It appears
          that lxml is faster. Investigate.
    '''

    # How to log
    # https://www.digitalocean.com/community/tutorials/how-to-use-logging-in-python-3
    import logging
    logger = logging.getLogger(__name__)
    # CHANGE TO INFO IF YOU WANT TO SEE DEBUG AND INFO MESSAGES
    logging.basicConfig(level=logging.WARNING)


    ''' Initialize, empty, the list that this function will return. '''
    list_report = []


    ''' Import junos-eznc base function and open Netconf session.'''
    from jnpr.junos import Device
    try:
        Device.auto_probe = 5
        device = Device(host=address_ipv4, user=os_username, password=os_password, gather_facts=False)
        device.open()
    except Exception as err:
        list_report.append("WARNING, the following error has happened: " + str(err))
        return list_report



    ''' Retrieve information.'''
    from jnpr.junos.op.isis import IsisAdjacencyTable
    isis_adjacency_table = IsisAdjacencyTable(device).get()

    # The stability period is x days
    number_of_days = 5
    stability_period = number_of_days * (24*60*60)

    # Findout the time now and the year.
    import datetime
    now = datetime.datetime.now()
    current_year = now.year

    # Start the tests
    for adjacency in isis_adjacency_table:


        ''' TEST, IS-IS stability '''
        for adjacency_log in adjacency.adjacency_log:
            from datetime import datetime
            datetime_object = datetime.strptime(adjacency_log.when, '%a %b %d %H:%M:%S')

            '''
            Junipers report date for last adjanceny change as <day of week> <day of month> < month>
            Junipers do NOT report the year for the last adjanceny change. 

            This means that first we need to figure if the event took place
            this year or the previous.
            So, compare current month and month of event. If later is bigger
            than former, then the even took place last year.
            '''
            import datetime
            month_current = datetime.date.today().month
            logger.info('month_current variable is: %s', month_current)
            month_adjacency_log = datetime_object.month
            logger.info('month_adjacency_log variable is: %s', month_adjacency_log)
            if month_adjacency_log > month_current:
                logger.info('adjacency change occurred last year')
                last_year = datetime.date.today().year - 1
                logger.info('year for comparation is: %s', last_year)
                datetime_object = datetime_object.replace(year=last_year)
            else:
                logger.info('adjacency change occurred this year')
                this_year = datetime.date.today().year
                logger.info('year for comparation is: %s', this_year)
                datetime_object = datetime_object.replace(year=current_year)



            period_last_reset = now - datetime_object
            logger.info('period_last_reset: %s', period_last_reset)
            delta_seconds = period_last_reset.total_seconds()
            delta_seconds = int(delta_seconds)
            logger.info('delta_seconds: %s', delta_seconds)

        if delta_seconds > stability_period:
            list_report.append("PASS, IS-IS stability in " + 
                adjacency.interface_name + 
                ". IS-IS has been stable for longer than " + 
                str(number_of_days) + " days. Adjacency has been " + 
                adjacency_log.state + " since " + adjacency_log.when + "."
            )
        else:
            list_report.append("FAIL, IS-IS stability in " +
                adjacency.interface_name +
                ". IS-IS has not been stable for longer than " +
                str(number_of_days) + " days. Adjacency has been " +
                adjacency_log.state + " since " + adjacency_log.when + "."
            )
            #list_report.append("FAIL, IS-IS has not been stable for longer than " + 
            #    str(number_of_days) + " days. Adjacency has been " + 
            #    adjacency_log.state + " since " + adjacency_log.when + "."
            #)



        ''' TEST, IS-IS Level seen and expected are the same.'''
        isis_settings['level'] = str(isis_settings['level'])
        adjacency.level = str(adjacency.level)
        if adjacency.level == isis_settings['level']:
            list_report.append("PASS, IS-IS Level in " + 
                adjacency.interface_name + ". IS-IS Level expected: " + 
                isis_settings['level'] + ". IS-IS Level seen: " + adjacency.level
            )
        else:
            list_report.append("FAIL, IS-IS Level in " + 
                adjacency.interface_name + ". IS-IS Level expected: " + 
                isis_settings['level'] + ". IS-IS Level seen: " + adjacency.level
            )



        ''' TEST, IS-IS circuit-type seen and expected are the same.'''
        isis_settings['circuit_type'] = str(isis_settings['circuit_type'])
        adjacency.circuit_type = str(adjacency.circuit_type)
        if adjacency.circuit_type == isis_settings['circuit_type']:
            list_report.append("PASS, IS-IS Circuit Type in " + 
                adjacency.interface_name + ". IS-IS Circuit Type expected: " + 
                isis_settings['circuit_type'] + ". IS-IS Circuit Type seen: " + 
                adjacency.circuit_type
            )
        else:
            list_report.append("FAIL, IS-IS Circuit Type in " + 
                adjacency.interface_name + ". IS-IS Circuit Type expected: " + 
                isis_settings['circuit_type'] + ". IS-IS Circuit Type seen: " + 
                adjacency.circuit_type
        )
    ''' refactor, end '''



    ''' TEST, IS-IS Level 1 LSP is Zero.'''
    '''
    Retrieve the full IS-IS database.
    Count the number of Level 1 LSP in the database.
    Verify the number of Level 1 LSP is Zero (0).
    '''


    ''' Find out what type of chassis we are dealing with '''
    from lxml import etree
    chassis_inventory = device.rpc.get_chassis_inventory()
    for element in chassis_inventory.findall('.//chassis'):
        chassis_description = element.find('description').text

    if chassis_description == 'ACX5048':
        '''
        The ACX5048 are giving grief and do not return the isis database correctly.
        If asked with format json, the ACX will give an error.
        If asked with format text, or no format, the type is <class 'lxml.etree._Element'>
        FOR THE MOMENT THIS IS A BUG, A MISSING FEATURE OF TORQUE
        '''
        return list_report


    isis_database = device.rpc.get_isis_database_information({'format': 'json'})
    lsp_count_l1 = isis_database['isis-database-information'][0]['isis-database'][0]['lsp-count'][0]['data']
    logger.info('lsp_count_l1: %s', lsp_count_l1)

    if lsp_count_l1 != '0':
        list_report.append("FAIL, IS-IS LSDB, there are L1 LSPs in L1 the LSDB.")
    else:
        list_report.append("PASS, IS-IS LSDB, there are no L1 LSPs in L1 the LSDB.")

    #from pprint import pprint
    #pprint(isis_database)

    #etree.dump(isis_database)
    #print(isis_database.findtext("isis-database/lsp-count"))

    device.close()
    return list_report

'''
# mark
# To test this function, uncomment this block
####  CONSTANTS  ####
fqdn = 'edge1-testlab.nn.hea.net'
#fqdn = 'edge2-testlab.nn.hea.net'
#fqdn = 'edge3-testlab.nn.hea.net'
local_username = 'heanet'
local_password = 'KqV7X98v!'

#fqdn = 'edge4-testlab.nn.hea.net'
#fqdn = 'edge5-testlab.nn.hea.net'
#local_username = 'heanet'
#local_password = '$!3u$uxqDMTXzw9'

#fqdn = 'edge1-dcu-glasnevin.nn.hea.net'
#fqdn = 'edge1-dcu-spd2.nn.hea.net'
#fqdn = 'edge2-dcu.nn.hea.net'
#fqdn = 'dist1-lyit2.nn.hea.net'
#fqdn = 'rr1-pw.nn.hea.net'
#fqdn = 'core2-blanch.nn.hea.net'
#fqdn = 'core2-pw.nn.hea.net'
#local_username = 'rancid'
#local_password = '#pW5MV4G!q%3341sfsdFSS!@'


isis_settings = {}
isis_settings['level'] = 2
isis_settings['circuit_type'] = 2
####  CONSTANTS  ####
import socket

try:
    address_ip = (socket.gethostbyname(fqdn))
except Exception as err:
    print(str(err))

audit_report = audit_jnpr_isis(address_ip, local_username, local_password, isis_settings)
for i in audit_report:
    print(i)
'''

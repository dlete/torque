
def audit_jnpr_keywords(address_ipv4, os_username, os_password, words_do_exist, words_no_exist, keyfiles_do_exist, keyfiles_no_exist):
    '''
    Search for occurrences of keywords in configuration.

    Retrieves the full configuration of a Ne. Puts the configuration in flat text.
    Parses the configuration for occurrences of keywords.

    Args:
        address_ip (str)
        os_username (str)
        os_password (str)
        words_do_exist(list)
        words_no_exist(list)
        keyfiles_do_exist(dict)
        keyfiles_no_exist(dict)

    Returns:
        list: each item in the list is a line of text. Each line of text begins
        with either of the keywords: PASS, FAIL, or WARNING. These first
        keywords are always in capital letters.

    To-do:
        - Consitent use of list or dictionary in keyXXX_do|no_exist. Either all
        list or all dict. Maybe make keyfiles a list of dictionaries?.
        - in arguments, use keywords instead of words.

    References:
        https://gist.github.com/jeffbrl/50b67dbe87bd08aea032
        https://www.juniper.net/documentation/en_US/junos-pyez/topics/example/junos-pyez-program-configuration-rescue-saving.html
        http://eli.thegreenplace.net/2012/03/15/processing-xml-in-python-with-elementtree
        https://docs.python.org/3/library/xml.etree.elementtree.html
    '''


    ''' Initialize, empty, the list that this function will return. '''
    list_report = []


    ''' Import junos-eznc base function and open Netconf session.'''
    from jnpr.junos import Device
    try:
        Device.auto_probe = 5
        device = Device(
            host=address_ipv4, 
            user=os_username,
            password=os_password,
            gather_facts=False
        )
        device.open()
    except Exception as err:
        list_report.append("WARNING, the following error has happened: " + str(err))
        return list_report


    config = device.rpc.get_config()
    from lxml import etree
    #uconfig = etree.tostring(config, encoding='unicode')
    #print(uconfig)

    #print("Next is device.facts['model']")
    #print(device.facts['model'])
    #print(device.facts['RE0']['model'])

    ''' Find out what type of chassis we are dealing with '''
    from lxml import etree
    chassis_inventory = device.rpc.get_chassis_inventory()
    for element in chassis_inventory.findall('.//chassis'):
        chassis_description = element.find('description').text

    #if device.facts['model'] == 'ACX2200':
    if (chassis_description == 'ACX2200'):
        words_do_exist.append('record-optics.slax')
        words_do_exist.append('PIC.message')
        keyfiles_do_exist['record-optics.slax'] = '/var/run/scripts/event/'
        #print("We found an ACX2200")
        #print(words_do_exist)
        #print(keyfiles_do_exist)
    #if device.facts['model'] is None:
    #    if "ACX5K" in device.facts['RE0']['model']:
    #        words_do_exist.append('record-optics.slax')
    #        keyfiles_do_exist['record-optics.slax'] = '/var/run/scripts/event/'
    if (chassis_description == 'ACX5048'):
        words_do_exist.append('record-optics.slax')
        keyfiles_do_exist['record-optics.slax'] = '/var/run/scripts/event/'



    words_do_exist_dict = {}
    for word in words_do_exist:
        words_do_exist_dict[word] = 0

    words_no_exist_dict = {}
    for word in words_no_exist:
        words_no_exist_dict[word] = 0


    for elem in config.iter():

        for word in words_do_exist:
            if elem.get(word) == word:
                #list_report.append("PASS, there is an occurence of " + word + " in the configuration")
                words_do_exist_dict[word] = words_do_exist_dict[word] + 1
            if elem.text == word:
                #list_report.append("PASS, there is an occurence of " + word + " in the configuration")
                words_do_exist_dict[word] = words_do_exist_dict[word] + 1

        for word in words_no_exist:
            if elem.get(word) == word:
                #list_report.append("FAIL, there is an occurence of " + word + " in the configuration")
                words_no_exist_dict[word] = words_no_exist_dict[word] + 1


    #print("These are the words that SHOULD exist")
    for key, value in words_do_exist_dict.items():
        #print("This is the key: " + key + ", and this is the value: " + str(value))
        if value == 0:
            if key == 'PIC.message':
                list_report.append("FAIL, JUNOS configuration snippet to automatically change the media-type in ACX2200 is not in place. Do review the 'event-options' hierarchy.")
            else:
                list_report.append("FAIL, there is no occurence of " + key + " in the configuration.")
                #print("value is 0 and key is " + key)
        elif value > 0:
            if key == 'PIC.message':
                list_report.append("PASS, JUNOS configuration snippet to automatically change the media-type in ACX2200 is in place.")
            else:
                list_report.append("PASS, there are " + str(value) + " occurence(s) of " + key + " in the configuration.")
                #print("value is bigger than 0 and key is " + key)
        else:
            list_report.append("WARNING, cannot determine if there is an occurrence or not of " + key + " in the configuration.")
            #print("value I do not know")


    #print("These are the words that should NOT exist")
    for key, value in words_no_exist_dict.items():
        #print("This is the key: " + key + ", and this is the value: " + str(value))
        if value == 0:
            list_report.append("PASS, there is no occurence of " + key + " in the configuration.")
        elif value > 0:
            list_report.append("FAIL, there are " + str(value) + " occurence(s) of " + key + " in the configuration.")
        else:
            list_report.append("WARNING, cannot determine if there is an occurrence or not of " + key + " in the configuration.")

    ########################## FILES SECTION
    #print("Next is keyfiles_do_exist, should be a dictionary")
    #print(keyfiles_do_exist)

    from jnpr.junos.utils.fs import FS
    #file_do_exist = 'record-optics.slax'
    #file_do_exist = 'file_that_should_exist.slax'
    #remote_path = '/var/run/scripts/event/'
    #fs = FS(device)
    #fs_files = fs.ls(path=remote_path, brief=False)

    #import pprint
    #pprint.pprint(fs_files)
    '''
    IF brief=True THE OUTPUT LOOKS LIKE:
    {'file_count': 1,
     'files': ['record-optics.slax'],
     'path': '/var/run/scripts/event/',
     'size': 15308,
     'type': 'dir'}

    IF brief=False THE OUTPUT LOOKS LIKE:
    {'file_count': 1,
     'files': {'record-optics.slax': {'owner': 'fallbackadmin',
                                      'path': 'record-optics.slax',
                                      'permissions': 644,
                                      'permissions_text': '-rw-r--r--',
                                      'size': 15308,
                                      'ts_date': 'May 30 16:18',
                                      'ts_epoc': '1496157510',
                                      'type': 'file'}},
     'path': '/var/run/scripts/event/',
     'size': 15308,
     'type': 'dir'}
    '''

    '''
    if file_do_exist in fs_files['files']:
        list_report.append("PASS, the file " + file_do_exist + " is in " + remote_path)
        print("Ole")
    else:
        list_report.append("FAIL, the file " + file_do_exist + " is NOT in " + remote_path)
    '''

    fs1 = FS(device)
    for key, value in keyfiles_do_exist.items():
        fs_files = fs1.ls(path=value, brief=False)
        if key in fs_files['files']:
            list_report.append("PASS, the file " + key + " is in " + value)
        else:
            list_report.append("FAIL, the file " + key + " is not in " + value)



    ########################## FILES SECTION

    try:
        device.close()
    except Exception as err:
        list_report.append("WARNING, the following error has happened: " + str(err))
        return list_report

    return list_report

'''
# mark
# To test this function, uncomment this block
####  CONSTANTS  ####
#fqdn = 'edge1-testlab.nn.hea.net'
fqdn = 'edge2-testlab.nn.hea.net'
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

#words_do_exist = ['record-optics.slax', 'word_that_should_exist_but_does_not_exist']
#words_do_exist = ['heanet-super-user', 'word_that_should_exist_but_does_not_exit']
words_do_exist = ['heanet-super-user']
#words_no_exist = ['inactive', 'word_that_should_no_exist_and_does_not_exit']
words_no_exist = ['inactive']

keyfiles_do_exist = {}
#keyfiles_do_exist['record-optics.slax'] = '/var/run/scripts/event/'
#keyfiles_do_exist['file_that_should_exist2.slax'] = '/var/run/scripts/event/'

keyfiles_no_exist = {}
####  CONSTANTS  ####


import socket

try:
    address_ipv4 = (socket.gethostbyname(fqdn))
except Exception as err:
    print(str(err))

audit_report = audit_jnpr_keywords(address_ipv4, local_username, local_password, words_do_exist, words_no_exist, keyfiles_do_exist, keyfiles_no_exist)
for i in audit_report:
    print(i)
'''

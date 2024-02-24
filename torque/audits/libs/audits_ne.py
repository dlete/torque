# Standard Python imports
'''Need this to timestamp the reports.'''
from datetime import datetime

# Core Django imports
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import render

# This project apps imports
#from inventory.models import Ne
from inventories.models import Ne


def get_me_ne_attributes(ne_id):
    ''' Returns a dictionary with many parameters for a given Ne.

    Pass ne_id as argument. With ne_id, get the ne object. Once you have the Ne
    object do find out its IP address, hostname, nni_neighbors, etc.

    Args:
        ne_id:  (str)
    Returns:
        ne_dict (dict)
    '''

    ''' Initialize, empty, the dictionary that the function will return. '''
    ne_dict = {}

    ''' Get the Ne object. Use get_object_or_404 helper to avoid try/except. '''
    ne = get_object_or_404(Ne, pk=ne_id)

    ''' For Ne object, get its IP address. '''
    try:
        import socket
        # https://docs.python.org/3/library/socket.html#socket.socket.settimeout
        # does not work when set. If set, regardless of the number of seconds, it will go directly into a fault
        #socket.settimeout(4)
        address_ipv4 = socket.gethostbyname(ne.fqdn)
        ''' To get the IPv6 address '''
        #address_ipv6 = socket.getaddrinfo(ne.fqdn, None, socket.AF_INET6)[0][4][0]
    except:
        raise Http404("Does not seem to be name resolution.")

    ''' For Ne object, get username and password. '''
    username = ne.os_credential.username
    password = ne.os_credential.password


    ''' For Ne, get nni_neighbors. '''
    nni_neighbors_expected = list(ne.nni_neighbors.values_list('fqdn', flat=True))
    #print(type(nni_neighbors_expected))
    #print(nni_neighbors_expected)
    #for n in nni_neighbors_expected:
    #    print(n.split('.')[0])
    #    print(n)
    # https://stackoverflow.com/questions/19290762/cant-modify-list-elements-in-a-loop-python
    nni_neighbors_expected = [n.split('.')[0] for n in nni_neighbors_expected]
    #print("this is the transformed list")
    #print(nni_neighbors_expected)

    ''' Now that we have all the Ne parameters, pack them into dictionary and
    return it to whoever invoked this function. '''
    ne_dict['address_ipv4'] = address_ipv4
    ne_dict['username'] = username
    ne_dict['password'] = password
    ne_dict['nni_neighbors'] = nni_neighbors_expected

    return ne_dict


def get_me_overall_audit_result(report_list):
    ''' Return either "PASS" or "FAIL".

    Look for the keywords "PASS", "FAIL" and "WARNING" in a given list. If you
    find find the keywords "FAIL" or "WARNING", return "FAIL"; otherwise,
    return "PASS".

    Args:
        report_list (list)
    Returns:
        overall_audit_result (str)
    '''

    number_of_fail = 0
    number_of_pass = 0
    number_of_warning = 0
    number_of_empty = 0
    number_of_inconclusive = 0

    for item in report_list:
        # IMPORTANT => LOGICAL OR IS NOT EVALUATED FOR THE IF CONDITION!!!!!!
        #if ("FAIL" or "WARNING") in item:
        if "FAIL" in item:
            number_of_fail = number_of_fail + 1
        elif "PASS" in item:
            number_of_pass = number_of_pass + 1
        elif "WARNING" in item:
            number_of_warning = number_of_warning + 1
        elif item is None:
            number_of_empty = number_of_empty + 1
        else:
            number_of_inconclusive = number_of_inconclusive + 1

    if number_of_fail > 0:
        overall_audit_result = "FAIL"
    elif number_of_pass > 0:
        overall_audit_result = "PASS"
    else:
        overall_audit_result = "WARNING"

    return overall_audit_result


def get_me_result_blocks(report_list):
    '''
    Args:
        report_list (list)
    Returns:
        report_dict (dict)
    '''

    ''' Initialize, empty, the dictionary that the function will return. '''
    report_dict = {}
    report_list_fail = []
    report_list_pass = []
    report_list_warning = []

    ''' Go through the list looking for keywords and putt the items in the
    corresponding list. '''
    for item in report_list:
        if "FAIL" in item:
            report_list_fail.append(item)
        elif "PASS" in item:
            report_list_pass.append(item)
        elif "WARNING" in item:
            report_list_warning.append(item)
        else:
            report_list_warning.append(item)

    ''' Now that we have each of the lists populated, pack them into the
    dictionary and return it to whoever invoked this function. '''
    report_dict['fail'] = report_list_fail
    report_dict['pass'] = report_list_pass
    report_dict['warning'] = report_list_warning

    return report_dict


def post_mail(mail_subject, mail_body):
    '''Send a mail with the Subject and Body we got as Args.

    Vars:
        mail_subject (str)
        mail_body (dict)
    Returns:
        Send a mail with the Subject and Body we got as Args.
    '''

    from django.core.mail import EmailMessage
    from django.template.loader import get_template
    #subject = "Audit report for " + ne.fqdn + " on " + context['report_timestamp'].strftime("%y-%m-%d %H:%M")
    subject = mail_subject
    #to = ['daniel.lete@heanet.ie']
    to = ['heanet-rman-audit@listserv.heanet.ie']
    #from_email = 'torque@presto.heanet.ie'
    from_email = 'torque@heanet.ie'
    #from_email = 'noreply@heanet.ie'
    ctx = mail_body
    #message = get_template('inventory/audit_report_email.html').render(ctx)
    message = get_template('inventories/audit_report_email.html').render(ctx)
    msg = EmailMessage(subject, message, to=to, from_email=from_email)
    msg.content_subtype = 'html'
    msg.send()
    #print("this print is from function post_mail to indicate it has been successful")


def ne_audit_bogus(ne_id):
    ne = get_object_or_404(Ne, pk=ne_id)
    context = {'bodymessage': ne.fqdn + ", Pigs in Space audit report"}
    context['report_timestamp'] = datetime.now()

    #from core.cli.libs.scraps import bogus_audit
    from core.libs.jnpr import bogus_audit
    report_list = bogus_audit.audit_pigs_in_space(int(ne_id)*9)

    report_dict = get_me_result_blocks(report_list)
    context['report_pass'] = report_dict['pass']
    context['report_fail'] = report_dict['fail']
    context['report_warning'] = report_dict['warning']

    # give the ne_id to the html template so that you can call the ne_detail back
    context['ne_fqdn'] = ne.fqdn
    context['ne_id'] = ne_id
    context['audit_report'] = report_list
    context['overall_audit_result'] = get_me_overall_audit_result(report_list)

    import time
    time.sleep(1)

    #mail_subject = context['overall_audit_result'] + ", audit Bogus report for " + ne.fqdn + " on " + context['report_timestamp'].strftime("%y-%m-%d %H:%M")
    #mail_body = context
    #post_mail(mail_subject, mail_body)

    return context

def ne_audit_all(ne_id):
    ne = get_object_or_404(Ne, pk=ne_id)
    context = {'bodymessage': ne.fqdn + ", All and everything audit report"}
    context['report_timestamp'] = datetime.now()

    ne_params = get_me_ne_attributes(ne_id)

    report_list = []
    ibgp_peers_expected = ['87.44.48.5', '87.44.48.6', '2001:770:200::5', '2001:770:200::6']

    from core.libs.jnpr.audit_jnpr_bgp import audit_jnpr_ibgp
    report_audit_ibgp = audit_jnpr_ibgp(ne_params['address_ipv4'],
        ne_params['username'], ne_params['password'], ibgp_peers_expected
    )
    report_list = report_list + report_audit_ibgp


    from core.libs.jnpr.audit_jnpr_chassis_alarms import audit_jnpr_chassis_alarms
    report_audit_chassis_alarms = audit_jnpr_chassis_alarms(ne_params['address_ipv4'],
        ne_params['username'], ne_params['password']
    )
    report_list = report_list + report_audit_chassis_alarms


    from core.libs.jnpr.audit_jnpr_duplicate_ip import audit_jnpr_duplicate_ip
    report_audit_duplicate_ip = audit_jnpr_duplicate_ip(ne_params['address_ipv4'],
        ne_params['username'], ne_params['password']
    )
    report_list = report_list + report_audit_duplicate_ip


    from core.libs.jnpr.audit_jnpr_isis import audit_jnpr_isis
    isis_settings = {}
    isis_settings['level'] = 2
    isis_settings['circuit_type'] = 2
    report_audit_isis = audit_jnpr_isis(ne_params['address_ipv4'],
        ne_params['username'], ne_params['password'], isis_settings
    )
    report_list = report_list + report_audit_isis


    from core.libs.jnpr.audit_jnpr_keywords import audit_jnpr_keywords
    keywords_do_exist = ['heanet-super-user']
    keywords_no_exist = ['inactive']
    keyfiles_do_exist = {}
    keyfiles_no_exist = {}
    report_audit_keywords = audit_jnpr_keywords(ne_params['address_ipv4'],
        ne_params['username'], ne_params['password'],
        keywords_do_exist, keywords_no_exist,
        keyfiles_do_exist, keyfiles_no_exist
    )
    report_list = report_list + report_audit_keywords


    from core.libs.jnpr.audit_jnpr_lldp import audit_jnpr_lldp
    report_audit_lldp = audit_jnpr_lldp(ne_params['address_ipv4'],
        ne_params['username'], ne_params['password'],
        ne_params['nni_neighbors'],
    )
    report_list = report_list + report_audit_lldp


    from core.libs.jnpr.audit_jnpr_nni_desc import audit_jnpr_nni_desc
    report_audit_nni_description = audit_jnpr_nni_desc(ne_params['address_ipv4'],
        ne_params['username'], ne_params['password']
    )
    report_list = report_list + report_audit_nni_description


    from core.libs.jnpr.audit_jnpr_os import audit_jnpr_os
    report_audit_os = audit_jnpr_os(ne_params['address_ipv4'],
        ne_params['username'], ne_params['password']
    )
    report_list = report_list + report_audit_os


    from core.libs.jnpr.audit_jnpr_phyport import audit_jnpr_phyport
    report_audit_phyport = audit_jnpr_phyport(ne_params['address_ipv4'],
        ne_params['username'], ne_params['password']
    )
    report_list = report_list + report_audit_phyport

    from core.libs.jnpr.audit_jnpr_phyport_stability import audit_jnpr_phyport_stability
    report_audit_phyport_stability = audit_jnpr_phyport_stability(ne_params['address_ipv4'],
        ne_params['username'], ne_params['password']
    )
    report_list = report_list + report_audit_phyport_stability

    from core.libs.jnpr.audit_jnpr_intopticdiag import audit_jnpr_intopticdiag
    report_audit_intopticdiag = audit_jnpr_intopticdiag(ne_params['address_ipv4'],
        ne_params['username'], ne_params['password'],
    )
    report_list = report_list + report_audit_intopticdiag

    from core.libs.jnpr.audit_jnpr_pic import audit_jnpr_transceiver
    report_audit_transceiver = audit_jnpr_transceiver(ne_params['address_ipv4'],
        ne_params['username'], ne_params['password']
    )
    report_list = report_list + report_audit_transceiver

    report_dict = get_me_result_blocks(report_list)
    context['report_pass'] = report_dict['pass']
    context['report_fail'] = report_dict['fail']
    context['report_warning'] = report_dict['warning']

    # pass the ne_id to the html template so that you can call the ne_detail back
    context['ne_fqdn'] = ne.fqdn
    context['ne_id'] = ne_id
    context['audit_report'] = report_list
    context['overall_audit_result'] = get_me_overall_audit_result(report_list)

    '''send mail with audit report '''
    mail_subject = context['overall_audit_result'] + ", audit All report for " + ne.fqdn + " on " + context['report_timestamp'].        strftime("%y-%m-%d %H:%M")
    mail_body = context
    post_mail(mail_subject, mail_body)

    return context



def ne_audit_chassis_alarms(ne_id):
    ne = get_object_or_404(Ne, pk=ne_id)
    context = {'bodymessage': ne.fqdn + ", Chassis Alarms audit report"}
    context['report_timestamp'] = datetime.now()

    ne_params = get_me_ne_attributes(ne_id)

    from core.libs.jnpr.audit_jnpr_chassis_alarms import audit_jnpr_chassis_alarms
    report_list = audit_jnpr_chassis_alarms(ne_params['address_ipv4'],
        ne_params['username'], ne_params['password']
    )
    report_dict = get_me_result_blocks(report_list)
    context['report_pass'] = report_dict['pass']
    context['report_fail'] = report_dict['fail']
    context['report_warning'] = report_dict['warning']

    # pass the ne_id to the html template so that you can call the ne_detail back
    context['ne_fqdn'] = ne.fqdn
    context['ne_id'] = ne_id
    context['audit_report'] = report_list
    context['overall_audit_result'] = get_me_overall_audit_result(report_list)

    return context



def ne_audit_duplicate_ip(ne_id):
    ne = get_object_or_404(Ne, pk=ne_id)
    context = {'bodymessage': ne.fqdn + ", IP Consistency audit report"}
    context['report_timestamp'] = datetime.now()

    ne_params = get_me_ne_attributes(ne_id)

    from core.libs.jnpr.audit_jnpr_duplicate_ip import audit_jnpr_duplicate_ip
    report_list = audit_jnpr_duplicate_ip(ne_params['address_ipv4'],
        ne_params['username'], ne_params['password']
    )
    report_dict = get_me_result_blocks(report_list)
    context['report_pass'] = report_dict['pass']
    context['report_fail'] = report_dict['fail']
    context['report_warning'] = report_dict['warning']

    # pass the ne_id to the html template so that you can call the ne_detail back
    context['ne_fqdn'] = ne.fqdn
    context['ne_id'] = ne_id
    context['audit_report'] = report_list
    context['overall_audit_result'] = get_me_overall_audit_result(report_list)

    return context



def ne_audit_ibgp(ne_id):
    ne = get_object_or_404(Ne, pk=ne_id)
    context = {'bodymessage': ne.fqdn + ", iBGP audit report"}
    context['report_timestamp'] = datetime.now()

    ne_params = get_me_ne_attributes(ne_id)
    ibgp_peers_expected = ['87.44.48.5', '87.44.48.6', '2001:770:200::5', '2001:770:200::6']

    from core.libs.jnpr.audit_jnpr_bgp import audit_jnpr_ibgp
    report_list = audit_jnpr_ibgp(ne_params['address_ipv4'],
        ne_params['username'], ne_params['password'], ibgp_peers_expected
    )
    report_dict = get_me_result_blocks(report_list)
    context['report_pass'] = report_dict['pass']
    context['report_fail'] = report_dict['fail']
    context['report_warning'] = report_dict['warning']

    # pass the ne_id to the html template so that you can call the ne_detail back
    context['ne_fqdn'] = ne.fqdn
    context['ne_id'] = ne_id
    context['audit_report'] = report_list
    context['overall_audit_result'] = get_me_overall_audit_result(report_list)
    return context


def ne_audit_intopticdiag(ne_id):
    ne = get_object_or_404(Ne, pk=ne_id)
    context = {'bodymessage': ne.fqdn + ", Interface Optical Diagnostics audit report"}
    context['report_timestamp'] = datetime.now()

    ne_params = get_me_ne_attributes(ne_id)

    from core.libs.jnpr.audit_jnpr_intopticdiag import audit_jnpr_intopticdiag
    report_audit_intopticdiag = audit_jnpr_intopticdiag(ne_params['address_ipv4'],
        ne_params['username'], ne_params['password'],
    )
    report_list = report_audit_intopticdiag

    report_dict = get_me_result_blocks(report_list)
    context['report_pass'] = report_dict['pass']
    context['report_fail'] = report_dict['fail']
    context['report_warning'] = report_dict['warning']

    # pass the ne_id to the html template so that you can call the ne_detail back
    context['ne_fqdn'] = ne.fqdn
    context['ne_id'] = ne_id
    context['audit_report'] = report_list
    context['overall_audit_result'] = get_me_overall_audit_result(report_list)
    return context



def ne_audit_isis(ne_id):
    ne = get_object_or_404(Ne, pk=ne_id)
    context = {'bodymessage': ne.fqdn + ", IS-IS audit report"}
    context['report_timestamp'] = datetime.now()

    ne_params = get_me_ne_attributes(ne_id)

    from core.libs.jnpr.audit_jnpr_isis import audit_jnpr_isis
    isis_settings = {}
    isis_settings['level'] = 2
    isis_settings['circuit_type'] = 2
    report_audit_isis = audit_jnpr_isis(ne_params['address_ipv4'],
        ne_params['username'], ne_params['password'], isis_settings
    )
    report_list = report_audit_isis

    report_dict = get_me_result_blocks(report_list)
    context['report_pass'] = report_dict['pass']
    context['report_fail'] = report_dict['fail']
    context['report_warning'] = report_dict['warning']

    # pass the ne_id to the html template so that you can call the ne_detail back
    context['ne_fqdn'] = ne.fqdn
    context['ne_id'] = ne_id
    context['audit_report'] = report_list
    context['overall_audit_result'] = get_me_overall_audit_result(report_list)
    return context


def ne_audit_keywords(ne_id):
    ne = get_object_or_404(Ne, pk=ne_id)
    context = {'bodymessage': ne.fqdn + ", Commands and Files audit report"}
    context['report_timestamp'] = datetime.now()

    ne_params = get_me_ne_attributes(ne_id)

    from core.libs.jnpr.audit_jnpr_keywords import audit_jnpr_keywords
    #keywords_do_exist = ['heanet-super-user', 'word_that_should_exist_but_does_not_exit']
    keywords_do_exist = ['heanet-super-user']
    #keywords_no_exist = ['inactive', 'word_that_should_no_exist_and_does_not_exit']
    keywords_no_exist = ['inactive']
    keyfiles_do_exist = {}
    #keyfiles_do_exist['file_that_should_exist2.slax'] = '/var/run/scripts/event/'
    keyfiles_no_exist = {}
    #keyfiles_no_exist['file_that_should_NOT_exist.slax'] = '/var/run/scripts/event/'
    report_list = audit_jnpr_keywords(ne_params['address_ipv4'],
        ne_params['username'], ne_params['password'],
        keywords_do_exist, keywords_no_exist, 
        keyfiles_do_exist, keyfiles_no_exist
    )

    report_dict = get_me_result_blocks(report_list)
    context['report_pass'] = report_dict['pass']
    context['report_fail'] = report_dict['fail']
    context['report_warning'] = report_dict['warning']

    # pass the ne_id to the html template so that you can call the ne_detail back
    context['ne_fqdn'] = ne.fqdn
    context['ne_id'] = ne_id
    context['audit_report'] = report_list
    context['overall_audit_result'] = get_me_overall_audit_result(report_list)

    return context


def ne_audit_lldp(ne_id):
    ne = get_object_or_404(Ne, pk=ne_id)
    context = {'bodymessage': ne.fqdn + ", LLDP audit report"}
    context['report_timestamp'] = datetime.now()

    ne_params = get_me_ne_attributes(ne_id)

    from core.libs.jnpr.audit_jnpr_lldp import audit_jnpr_lldp
    report_list = audit_jnpr_lldp(ne_params['address_ipv4'],
        ne_params['username'], ne_params['password'],
        ne_params['nni_neighbors'],
    )
    report_dict = get_me_result_blocks(report_list)
    context['report_pass'] = report_dict['pass']
    context['report_fail'] = report_dict['fail']
    context['report_warning'] = report_dict['warning']

    # pass the ne_id to the html template so that you can call the ne_detail back
    context['ne_fqdn'] = ne.fqdn
    context['ne_id'] = ne_id
    context['audit_report'] = report_list
    context['overall_audit_result'] = get_me_overall_audit_result(report_list)
    return context


def ne_audit_nni_description(ne_id):
    ''' Audits that NNI interface description contains a circuit id '''
    ne = get_object_or_404(Ne, pk=ne_id)
    context = {'bodymessage': ne.fqdn + ", NNI description audit report"}
    context['report_timestamp'] = datetime.now()

    ne_params = get_me_ne_attributes(ne_id)

    from core.libs.jnpr.audit_jnpr_nni_desc import audit_jnpr_nni_desc
    report_list = audit_jnpr_nni_desc(ne_params['address_ipv4'],
        ne_params['username'], ne_params['password']
    )
    report_dict = get_me_result_blocks(report_list)
    context['report_pass'] = report_dict['pass']
    context['report_fail'] = report_dict['fail']
    context['report_warning'] = report_dict['warning']

    # pass the ne_id to the html template so that you can call the ne_detail back
    context['ne_fqdn'] = ne.fqdn
    context['ne_id'] = ne_id
    context['audit_report'] = report_list
    context['overall_audit_result'] = get_me_overall_audit_result(report_list)
    return context


def ne_audit_os(ne_id):
    ne = get_object_or_404(Ne, pk=ne_id)
    context = {'bodymessage': ne.fqdn + ", Operating System audit report"}
    context['report_timestamp'] = datetime.now()

    ne_params = get_me_ne_attributes(ne_id)

    from core.libs.jnpr.audit_jnpr_os import audit_jnpr_os
    report_list = audit_jnpr_os(ne_params['address_ipv4'],
        ne_params['username'], ne_params['password']
    )
    report_dict = get_me_result_blocks(report_list)
    context['report_pass'] = report_dict['pass']
    context['report_fail'] = report_dict['fail']
    context['report_warning'] = report_dict['warning']

    # pass the ne_id to the html template so that you can call the ne_detail back
    context['ne_fqdn'] = ne.fqdn
    context['ne_id'] = ne_id
    context['audit_report'] = report_list
    context['overall_audit_result'] = get_me_overall_audit_result(report_list)
    return context


def ne_audit_phyport(ne_id):
    ne = get_object_or_404(Ne, pk=ne_id)
    context = {'bodymessage': ne.fqdn + ", PHYSICAL PORTS audit report"}
    context['report_timestamp'] = datetime.now()

    ne_params = get_me_ne_attributes(ne_id)

    from core.libs.jnpr.audit_jnpr_phyport import audit_jnpr_phyport
    report_audit_phyport = audit_jnpr_phyport(ne_params['address_ipv4'],
        ne_params['username'], ne_params['password']
    )
    from core.libs.jnpr.audit_jnpr_phyport_stability import audit_jnpr_phyport_stability
    report_audit_phyport_stability = audit_jnpr_phyport_stability(ne_params['address_ipv4'],
        ne_params['username'], ne_params['password']
    )

    report_list = report_audit_phyport + report_audit_phyport_stability

    report_dict = get_me_result_blocks(report_list)
    context['report_pass'] = report_dict['pass']
    context['report_fail'] = report_dict['fail']
    context['report_warning'] = report_dict['warning']

    # pass the ne_id to the html template so that you can call the ne_detail back
    context['ne_fqdn'] = ne.fqdn
    context['ne_id'] = ne_id
    context['audit_report'] = report_list
    context['overall_audit_result'] = get_me_overall_audit_result(report_list)
    return context


def ne_audit_transceiver(ne_id):
    ne = get_object_or_404(Ne, pk=ne_id)
    context = {'bodymessage': ne.fqdn + ", TRANSCEIVERS audit report"}
    context['report_timestamp'] = datetime.now()

    ne_params = get_me_ne_attributes(ne_id)

    from core.libs.jnpr.audit_jnpr_pic import audit_jnpr_transceiver
    report_list = audit_jnpr_transceiver(ne_params['address_ipv4'],
        ne_params['username'], ne_params['password']
    )
    report_dict = get_me_result_blocks(report_list)
    context['report_pass'] = report_dict['pass']
    context['report_fail'] = report_dict['fail']
    context['report_warning'] = report_dict['warning']

    # pass the ne_id to the html template so that you can call the ne_detail back
    context['ne_fqdn'] = ne.fqdn
    context['ne_id'] = ne_id
    context['audit_report'] = report_list
    context['overall_audit_result'] = get_me_overall_audit_result(report_list)
    return context

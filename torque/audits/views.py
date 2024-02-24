# Core Django imports
from django.shortcuts import render

# This project apps imports
from audits.libs import audits_ne

def ne_bogus(request, ne_id):
    '''
    Calls a function in another "module"?. The function returns a dictionary
    and we render that dictionary.
    '''
    from audits.libs import audits_ne
    context = audits_ne.ne_audit_bogus(ne_id)
    return render(request, 'audits/audit_report_blocks.html', context)
    

def ne_all(request, ne_id):
    from audits.libs import audits_ne
    context = audits_ne.ne_audit_all(ne_id)
    return render(request, 'audits/audit_report_blocks.html', context)


def ne_chassis_alarms(request, ne_id):
    from audits.libs import audits_ne
    context = audits_ne.ne_audit_chassis_alarms(ne_id)
    return render(request, 'audits/audit_report_blocks.html', context)


def ne_duplicate_ip(request, ne_id):
    from audits.libs import audits_ne
    context = audits_ne.ne_audit_duplicate_ip(ne_id)
    return render(request, 'audits/audit_report_blocks.html', context)


def ne_ibgp(request, ne_id):
    from audits.libs import audits_ne
    context = audits_ne.ne_audit_ibgp(ne_id)
    return render(request, 'audits/audit_report_blocks.html', context)


def ne_intopticdiag(request, ne_id):
    from audits.libs import audits_ne
    context = audits_ne.ne_audit_intopticdiag(ne_id)
    return render(request, 'audits/audit_report_blocks.html', context)


def ne_isis(request, ne_id):
    from audits.libs import audits_ne
    context = audits_ne.ne_audit_isis(ne_id)
    return render(request, 'audits/audit_report_blocks.html', context)


def ne_keywords(request, ne_id):
    from audits.libs import audits_ne
    context = audits_ne.ne_audit_keywords(ne_id)
    return render(request, 'audits/audit_report_blocks.html', context)


def ne_lldp(request, ne_id):
    from audits.libs import audits_ne
    context = audits_ne.ne_audit_lldp(ne_id)
    return render(request, 'audits/audit_report_blocks.html', context)


def ne_nni_description(request, ne_id):
    from audits.libs import audits_ne
    context = audits_ne.ne_audit_nni_description(ne_id)
    return render(request, 'audits/audit_report_blocks.html', context)


def ne_os(request, ne_id):
    from audits.libs import audits_ne
    context = audits_ne.ne_audit_os(ne_id)
    return render(request, 'audits/audit_report_blocks.html', context)


def ne_phyport(request, ne_id):
    from audits.libs import audits_ne
    context = audits_ne.ne_audit_phyport(ne_id)
    return render(request, 'audits/audit_report_blocks.html', context)


def ne_transceiver(request, ne_id):
    from audits.libs import audits_ne
    context = audits_ne.ne_audit_transceiver(ne_id)
    return render(request, 'audits/audit_report_blocks.html', context)

'''
http://docs.python-requests.org/en/master/user/authentication/
'''
import requests

username = 'admin'
password = 'Friday13'

# Get the list of all the ne.id
from requests.auth import HTTPBasicAuth
# works because: we bypass Apache and DRF is set to use authentication
#r = requests.get('http://192.168.56.102:3000/api/v1/inventories/ne/', auth=('admin', 'Friday13'))

# works if: Apache does not use authentication and DRF is set to use authentication
# works if: Apache DOES USE authentication and 'WSGIPassAuthorization On' is in apache2 conf and DRF is set to use authentication
#r = requests.get('http://192.168.56.102/api/v1/inventories/ne/', auth=('admin', 'Friday13'))

r = requests.get('http://checkme.heanet.ie/api/v1/inventories/ne/', auth=('admin', 'Friday13'))
# presto is 193.1.219.68
#r = requests.get('http://193.1.219.68/api/v1/inventories/ne/', auth=('admin', 'Friday13'))

#print("Next is r.status_code")
#print(r.status_code)
#print("Next is r.json()")
#print(r.json())

'''
#####################################################################
# THIS IS THE PART WHERE WE WORK WITH A SINGLE NE
# BEGIN
# edge3-testlab.nn.hea.net 448
# edge1-ipa.nn.hea.net 336
#base_url = 'http://192.168.56.102:3000/api/v1/audits/ne_bogus/'
#base_url = 'http://192.168.56.102:3000/api/v1/audits/ne_isis/'
base_url = 'http://checkme.heanet.ie/api/v1/audits/ne_ibgp/'
#base_url = 'http://checkme.heanet.ie/api/v1/audits/ne_isis/'
#ne_id = 448
ne_id = 336
url = base_url + str(ne_id) + '/'

report_text = ''

r = requests.get(url, auth=('admin', 'Friday13'))
audit_report_dict = r.json()

if 'detail' in audit_report_dict:
    #print("Super alerta!!, the dict is empty!!")
    #print("Next is audit_report_dict")
    #print(audit_report_dict)    # {'detail': 'Not found.'}
    report_text = "\n".join([report_text, "No connectivity to device with id " + str(ne_id)])
else:
    report_text = "\n".join([report_text, audit_report_dict['bodymessage']])

    if audit_report_dict['overall_audit_result'] == 'FAIL':
        report_text = "\n".join([report_text,"overall is a FAIL"])
        for l in audit_report_dict['report_fail']:
            report_text = "\n".join([report_text, l])
    elif audit_report_dict['overall_audit_result'] == 'PASS':
        report_text = "\n".join([report_text,"overall is a PASS"])
    elif audit_report_dict['overall_audit_result'] == 'WARNING':
        report_text = "\n".join([report_text,"overall is a WARNING"])
    else:
        report_text = "\n".join([report_text,"cant't determinte the outcome."])
print(report_text)
# END
#####################################################################
'''

'''
#####################################################################
# THIS IS THE PART WHERE WE WORK WITH A SUBSET OF NE
# BEGIN
# edge1-testlab.nn.hea.net 327
# edge2-testlab.nn.hea.net 437
# edge3-testlab.nn.hea.net 448
# edge1-ipa.nn.hea.net 336
#ids_to_run = [ '327', '437', '448' ]
#ids_to_run = [ '327', '336' ] 
ids_to_run = [ '327', '437', '448', '336' ]
#base_url = 'http://192.168.56.102:3000/api/v1/audits/ne_bogus/'
#base_url = 'http://192.168.56.102:3000/api/v1/audits/ne_ibgp/'
#base_url = 'http://192.168.56.102:3000/api/v1/audits/ne_isis/'
#base_url = 'http://checkme.heanet.ie/api/v1/audits/ne_ibgp/'
base_url = 'http://checkme.heanet.ie/api/v1/audits/ne_keywords/'
#base_url = 'http://checkme.heanet.ie/api/v1/audits/ne_isis/'

report_text = ''
report_text = "\n".join([report_text, "NE not listed below either PASS or are not connected."])
report_text = "\n\n".join([report_text,""])
total_ne = len(ids_to_run)
n = 0

for i in ids_to_run:
    url = base_url + str(i) + '/'

    r = requests.get(url, auth=('admin', 'Friday13'))
    audit_report_dict = r.json()

    if 'detail' in audit_report_dict:
        #report_text = "\n".join([report_text, "No connectivity to device with id " + str(i)])
        pass
    else:
        #report_text = "\n".join([report_text, audit_report_dict['bodymessage']])
        if audit_report_dict['overall_audit_result'] == 'FAIL':
            report_text = "\n".join([report_text, audit_report_dict['bodymessage']])
            report_text = "\n".join([report_text,"overall is a FAIL"])
            for l in audit_report_dict['report_fail']:
                report_text = "\n".join([report_text, l])
        elif audit_report_dict['overall_audit_result'] == 'PASS':
            #report_text = "\n".join([report_text, audit_report_dict['bodymessage']])
            #report_text = "\n".join([report_text,"overall is a PASS"])
            pass
        elif audit_report_dict['overall_audit_result'] == 'WARNING':
            report_text = "\n".join([report_text, audit_report_dict['bodymessage']])
            report_text = "\n".join([report_text,"overall is a WARNING"])
        else:
            report_text = "\n".join([report_text, audit_report_dict['bodymessage']])
            report_text = "\n".join([report_text,"cant't determinte the outcome."])

    n = n + 1
    print("Have just completed ne_id " + i + ", item " + str(n) + " of a total of " + str(total_ne) )

    report_text = "\n\n".join([report_text,""])

print(report_text)
# END
#####################################################################
'''

#####################################################################
# THIS IS THE FOR PART, WHERE WE WORK WITH ALL THE NE
# BEGIN
#base_url = 'http://checkme.heanet.ie/api/v1/audits/ne_bogus/'
base_url = 'http://checkme.heanet.ie/api/v1/audits/ne_all/'
#base_url = 'http://checkme.heanet.ie/api/v1/audits/ne_ibgp/'
#base_url = 'http://checkme.heanet.ie/api/v1/audits/ne_keywords/'
#base_url = 'http://checkme.heanet.ie/api/v1/audits/ne_isis/'

report_text = ''
report_text = "\n".join([report_text, "NE not listed below either PASS or are not connected."])
report_text = "\n\n".join([report_text,""])

total_ne = len(r.json())
n = 0

for i in r.json():
    # We have access to the fqdn and id of each Ne
    #print(i['fqdn'], i['id'])
    url = base_url + str(i['id']) + '/'
    #print(i['fqdn'], i['id'], url)

    r = requests.get(url, auth=('admin', 'Friday13'))
    audit_report_dict = r.json()

    if 'detail' in audit_report_dict:
        #report_text = "\n".join([report_text, "No connectivity to " + i['fqdn']])
        pass
    else:
        #report_text = "\n".join([report_text, audit_report_dict['bodymessage']])
        if audit_report_dict['overall_audit_result'] == 'FAIL':
            report_text = "\n".join([report_text, audit_report_dict['bodymessage']])
            report_text = "\n".join([report_text,"overall is a FAIL"])
            for l in audit_report_dict['report_fail']:
                report_text = "\n".join([report_text, l])
            report_text = "\n\n".join([report_text,""])
        elif audit_report_dict['overall_audit_result'] == 'PASS':
            #report_text = "\n".join([report_text, audit_report_dict['bodymessage']])
            #report_text = "\n".join([report_text,"overall is a PASS"])
            #report_text = "\n\n".join([report_text,""])
            pass
        elif audit_report_dict['overall_audit_result'] == 'WARNING':
            report_text = "\n".join([report_text, audit_report_dict['bodymessage']])
            report_text = "\n".join([report_text,"overall is a WARNING"])
            report_text = "\n\n".join([report_text,""])
        else:
            report_text = "\n".join([report_text, audit_report_dict['bodymessage']])
            report_text = "\n".join([report_text,"cant't determinte the outcome."])
            report_text = "\n\n".join([report_text,""])
    
    n = n + 1
    print("Have just completed " + i['fqdn'] + ", item " + str(n) + " of a total of " + str(total_ne) )

    #report_text = "\n\n\n".join([report_text,""])

# END
#####################################################################


#####################################################################
# THIS IS THE SENDING MAIL PART
# mainly: https://docs.python.org/3.4/library/email-examples.html
# marginally: http://naelshiab.com/tutorial-send-email-python/
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
fromaddr = 'torque_app@heanet.ie'
# [] DOES NOT WORK AT ALL!!!!!
#toaddrs  = ['daniel.lete@heanet.ie', 'daniel.lete@gmail.com']
# it wants things in this format (RFC822)
#toaddrs  = "daniel.lete@heanet.ie, daniel.lete@gmail.com"
#mail1 = 'daniel.lete@heanet.ie'
#mail2 = 'daniel.lete@gmail.com'
#toaddrs  = mail1 + ", " + mail2
toaddrs = 'daniel.lete@heanet.ie'
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddrs
from datetime import datetime
report_timestamp = datetime.now()
report_timestamp = report_timestamp.strftime("%Y-%b-%d %H:%M %p")
msg['Subject'] = "Audit report for RMAN NE on " + report_timestamp
#body = "YOUR MESSAGE HERE"
body = report_text

part1 = MIMEText(body, 'plain')
#msg.attach(MIMEText(body, 'plain'))
msg.attach(part1)

server = smtplib.SMTP('smtp.heanet.ie', 587)
#server.set_debuglevel(True) # show communication with the server
server.starttls()
server.login('torque_app', 'Fai4ohai!ph4wah9')
server.sendmail(fromaddr, toaddrs, msg.as_string())
server.quit()
# END
#####################################################################

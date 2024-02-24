
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
msg['Subject'] = "Keepalive Python Sendmail"
body = "YOUR MESSAGE HERE"
#body = report_text

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

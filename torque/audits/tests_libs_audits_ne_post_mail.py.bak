# NOTES
# bogus mail backend
# https://stackoverflow.com/questions/35958467/avoid-django-core-mail-outbox-as-e-mail-backend-in-test-execution-on-django



# Core Django imports
from django.core import mail
from django.test import TestCase

# This project apps imports
from audits.libs import audits_ne

context = {}
context['bodymessage'] = "Fake_FQDN" + ", Pigs in Space audit report"
from datetime import datetime
context['report_timestamp'] = datetime.now()
context['report_fail'] = [
    "FAIL, Pietro flies timidly",
    "FAIL, Sebastian runs supremely"
]
context['report_pass'] = [
    "PASS, Melody counts like a limp elephant",
    "PASS, Sebastian paints cockily",
    "PASS, Julie flies like a squirrel"
]
context['report_warning'] = [
    "WARNING, Pietro flies chancely"
]
context['ne_fqdn'] = "Fake_FQDN"
context['ne_id'] = "33"
context['audit_report'] = context['report_pass']
context['overall_audit_result'] = "PASS"


class AuditLibsAuditsNePostMailTests(TestCase):
#class EmailTest(TestCase):
    def test_send_email(self):
        # Send message.
        mail.send_mail(
            'Subject here', 'Here is the message.',
            'from@example.com', ['to@example.com'],
            fail_silently=False,
        )

        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)

        # Verify that the subject of the first message is correct.
        self.assertEqual(mail.outbox[0].subject, 'Subject here')


    def test_post_mail(self):
        mail_subject = "This is the Subject"
        mail_body = "This is the body"
        #outcome = audits_ne.post_mail(mail_subject, mail_body)
        outcome = audits_ne.post_mail(mail_subject, context)
        print(outcome)
        #print(len(mail.outbox))


# Core Django imports
from django.test import TestCase

# Third-party app imports


# This project apps imports
from audits.libs import audits_ne 

context = {}
context['bodymessage'] = "Fake_FQDN" + ", Pigs in Space audit report"
from datetime import datetime
context['report_timestamp'] = datetime.now()
context['report_pass'] = [
    "PASS, Melody counts like a limp elephant",
    "PASS, Sebastian paints cockily",
    "PASS, Julie flies like a squirrel"
]
context['report_fail'] = [
    "FAIL, Pietro flies timidly",
    "FAIL, Sebastian runs supremely"
]
context['report_warning'] = [
    "WARNING, Pietro flies chancely"
]
context['ne_fqdn'] = "Fake_FQDN"
context['ne_id'] = "33"
context['audit_report'] = context['report_pass']
context['overall_audit_result'] = "PASS"

wrong_context = {}
wrong_context['report_empty'] = []
wrong_context['report_nokeywords'] = [
    "BLAH, Otto spins gracefully",
    "BLAH, Sigfrid gardens like a bird"
]

class AuditLibsAuditsNeGetMeOverallAuditResultsTests(TestCase):
    '''
    Tests for the function get_me_overall_audit_result
    '''
    def test_overall_audit_result_all_fail(self):
        # Result list where all are a Fail should result in an overall Fail.
        audit_results = context['report_fail']
        outcome = audits_ne.get_me_overall_audit_result(audit_results)
        self.assertEqual(outcome, 'FAIL')

    def test_overall_audit_result_all_pass(self):
        # Result list where all are a Pass should result in an overall Pass.
        audit_results = context['report_pass']
        outcome = audits_ne.get_me_overall_audit_result(audit_results)
        self.assertEqual(outcome, 'PASS')

    def test_overall_audit_result_all_warning(self):
        # Result list where all are a Warning should result in an overall Pass.
        audit_results = context['report_warning']
        outcome = audits_ne.get_me_overall_audit_result(audit_results)
        self.assertEqual(outcome, 'WARNING')

    def test_overall_audit_result_fail_pass_warning(self):
        # Result list with at least a Fail should result in an overall Fail.
        audit_results = context['report_pass'] + context['report_fail'] + context['report_warning']
        outcome = audits_ne.get_me_overall_audit_result(audit_results)
        self.assertEqual(outcome, 'FAIL')

    def test_overall_audit_result_empty(self):
        audit_results = wrong_context['report_nokeywords']
        outcome = audits_ne.get_me_overall_audit_result(audit_results)
        self.assertEqual(outcome, 'WARNING')

    def test_overall_audit_result_nokeywords(self):
        audit_results = wrong_context['report_nokeywords']
        outcome = audits_ne.get_me_overall_audit_result(audit_results)
        self.assertEqual(outcome, 'WARNING')


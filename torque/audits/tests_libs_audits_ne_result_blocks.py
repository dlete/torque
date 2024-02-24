# Core Django imports
from django.test import TestCase

# Third-party app imports


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

wrong_context = {}
wrong_context['report_empty'] = []
wrong_context['report_nokeywords'] = [
    "BLAH, Otto spins gracefully",
    "BLAH, Sigfrid gardens like a bird"
]

raw_results_list = context['report_fail'] + context['report_pass'] + context['report_warning'] + wrong_context['report_empty'] + wrong_context['report_nokeywords']

messy_input_list = wrong_context['report_empty'] + wrong_context['report_nokeywords']


class AuditLibsAuditsNeGetMeResultBlocksTests(TestCase):
    '''
    Tests for the function get_me_result_blocks
    '''

    def test_result_blocks_output_is_dictionary(self):
        '''
        Test that the output is a dictionary.
        '''
        my_blocks_dict = audits_ne.get_me_result_blocks(raw_results_list)
        self.assertIsInstance(my_blocks_dict, dict)


    def test_result_blocks_input_is_messy(self):
        '''
        Test messy input does result only in WARNING output.
        '''
        my_output = audits_ne.get_me_result_blocks(messy_input_list)
        empty_list = []

        self.assertIsInstance(my_output, dict)
        self.assertEqual(my_output['fail'], empty_list)
        self.assertEqual(my_output['pass'], empty_list)
        self.assertEqual(my_output['warning'], messy_input_list)


    def test_result_blocks_input_is_only_fail(self):
        '''
        Test input with only fails results in only FAIL output.
        '''
        my_output = audits_ne.get_me_result_blocks(context['report_fail'])
        empty_list = []

        self.assertIsInstance(my_output, dict)
        self.assertEqual(my_output['fail'], context['report_fail'])
        self.assertEqual(my_output['pass'], empty_list)
        self.assertEqual(my_output['warning'], empty_list)


    def test_result_blocks_input_is_only_pass(self):
        '''
        Test input with only passes results in only PASS output.
        '''
        my_output = audits_ne.get_me_result_blocks(context['report_pass'])
        empty_list = []

        self.assertIsInstance(my_output, dict)
        self.assertEqual(my_output['fail'], empty_list)
        self.assertEqual(my_output['pass'], context['report_pass'])
        self.assertEqual(my_output['warning'], empty_list)


    def test_result_blocks_input_is_only_warning(self):
        '''
        Test input with only warnings results in only WARNING output.
        '''
        my_output = audits_ne.get_me_result_blocks(context['report_warning'])
        empty_list = []

        self.assertIsInstance(my_output, dict)
        self.assertEqual(my_output['fail'], empty_list)
        self.assertEqual(my_output['pass'], empty_list)
        self.assertEqual(my_output['warning'], context['report_warning'])


    def test_result_blocks_input_is_varied(self):
        '''
        Test input has FAIL, PASS, WARNING, empty and wrong, result is
        dictionary with 'fail', 'pass' and 'warning' keys populated.
        '''
        my_blocks_dict = audits_ne.get_me_result_blocks(raw_results_list)

        self.assertIsInstance(my_blocks_dict, dict)
        self.assertEqual(my_blocks_dict['fail'], context['report_fail'])
        self.assertEqual(my_blocks_dict['pass'], context['report_pass'])

        expected_raw_warning_list = context['report_warning'] + wrong_context['report_empty'] + wrong_context['report_nokeywords']
        self.assertEqual(my_blocks_dict['warning'], expected_raw_warning_list)




    def test_result_blocks(self):
        my_blocks_dict = audits_ne.get_me_result_blocks(raw_results_list)
        #print("context['report_fail']")
        #print(context['report_fail'])
        #print("my_blocks_dict['fail']")
        #print(my_blocks_dict['fail'])
        self.assertIsInstance(my_blocks_dict['fail'], list)
        self.assertEqual(my_blocks_dict['fail'], context['report_fail'])

        #print("context['report_pass']")
        #print(context['report_pass'])
        #print("my_blocks_dict['pass']")
        #print(my_blocks_dict['pass'])
        self.assertIsInstance(my_blocks_dict['pass'], list)
        self.assertEqual(my_blocks_dict['pass'], context['report_pass'])

        expected_raw_warning_list = context['report_warning'] + wrong_context['report_empty'] + wrong_context['report_nokeywords']
        #print("expected_raw_warning_list")
        #print(expected_raw_warning_list)
        #print("my_blocks_dict['warning']")
        #print(my_blocks_dict['warning'])
        self.assertIsInstance(my_blocks_dict['warning'], list)
        self.assertEqual(my_blocks_dict['warning'], expected_raw_warning_list)

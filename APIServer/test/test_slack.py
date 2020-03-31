import unittest

import responses

from APIServer.commons.api_utils import read_json
from APIServer.slack.push import send_slack_log, send_json_to_slack_channel, open_form
from APIServer.slack.format import create_alert_from_slack_message, get_id_from_payload
from APIServer.slack.format import slack_format_alert, create_updated_alert_from_slack_message


test_config_path = 'test_data/test_slack.json'
sample_alert_json_path = 'test_data/test_json.json'
slack_config = read_json(test_config_path)
sample_alert_json = read_json(sample_alert_json_path)


class TestCase(unittest.TestCase):

    @responses.activate
    def testLog(self):
        """
        Testing if send_slack_log works
        """
        responses.add(**{
            'method'         : responses.POST,
            'url'            : slack_config['url'],
            'body'           : 'ok',
            'status'         : 200,
            'content_type'   : 'application/json'
        })
        response = send_slack_log('Hello, Socnet')
        self.assertEqual('ok', response[200])


    @responses.activate
    def testPush(self):
        """
        Testing if send_json_to_slack_channel works
        """
        responses.add(**{
            'method'         : responses.POST,
            'url'            : 'https://slack.com/api/chat.postMessage',
            'body'           : 'ok',
            'status'         : 200,
            'content_type'   : 'application/json'
        })
        response = send_json_to_slack_channel({'text': 'Hello, Socnet'}, 'my_channel')
        self.assertEqual('ok', response[200])


    @responses.activate
    def testOpenForm(self):
        """
        Testing if open_form works
        """
        responses.add(**{
            'method'         : responses.POST,
            'url'            : 'https://slack.com/api/views.open',
            'body'           : 'ok',
            'status'         : 200,
            'content_type'   : 'application/json'
        })
        response = open_form('my_channel', 'my_tigger_id', 'test_data/slack/post_alert_form.json')
        self.assertEqual('ok', response[200])


    def testCreateAlertFromSlack(self):
        """
        Testing if create_alert_from_slack_message works
        """
        payload = slack_config['modal_submission_payload']
        time = '2019-11-01 17:45:32'
        alert_json = create_alert_from_slack_message(payload, time)
        self.assertEqual(sample_alert_json, alert_json)


    def testFormatAlert(self):
        """
        Testing if slack_format_alert works
        """
        ret = slack_format_alert([])
        self.assertEqual('This alert does not exist or has been deleted.', ret['text'])
        ret = slack_format_alert([(1,'2020-03-04 17:54:20', '10001',
                                'New York City', 'New York', 'USA', 'Fire', 'Fire in the building',
                                'High', 'Socnet Tester')])
        sample_message_path = 'test_data/slack/formatted_slack_message.json'
        sample_message = read_json(sample_message_path)
        self.assertEqual(sample_message, ret)



import unittest

import responses

from APIServer.commons.api_utils import read_json
from APIServer.slack.push import send_slack_log
from APIServer.slack.push import send_json_to_slack_channel
from APIServer.slack.push import open_form
from APIServer.slack.push import get_confirmation_form
from APIServer.slack.format import slack_format_alert
from APIServer.slack.format import create_alert_from_slack_message
from APIServer.slack.format import create_updated_alert_from_slack_message
from APIServer.slack.format import get_id_from_payload

SLACK_CONFIG_PATH = 'test_data/slack/test_slack.json'
SAMPLE_ALERT_JSON_PATH = 'test_data/test_json.json'
POST_ALERT_PAYLOAD_PATH = 'test_data/slack/post_alert_payload.json'
UPDATE_ALERT_PAYLOAD_PATH = 'test_data/slack/update_alert_payload.json'
SAMPLE_MESSAGE_PATH = 'test_data/slack/formatted_slack_message.json'
TIME = '2019-11-01 17:45:32'
slack_config = read_json(SLACK_CONFIG_PATH)
sample_alert_json = read_json(SAMPLE_ALERT_JSON_PATH)
post_alert_payload = read_json(POST_ALERT_PAYLOAD_PATH)
update_alert_payload = read_json(UPDATE_ALERT_PAYLOAD_PATH)
sample_message = read_json(SAMPLE_MESSAGE_PATH)


class TestSlack(unittest.TestCase):

    @responses.activate
    def testLog(self):
        """
        Testing if send_slack_log works
        """
        responses.add(**{
            'method': responses.POST,
            'url': slack_config['Log_URL'],
            'body': 'ok',
            'status': 200,
            'content_type': 'application/json'
        })
        response = send_slack_log('Hello, Socnet')
        self.assertEqual('ok', response[200])

    @responses.activate
    def testPush(self):
        """
        Testing if send_json_to_slack_channel works
        """
        responses.add(**{
            'method': responses.POST,
            'url': slack_config['Post_Chat_URL'],
            'body': 'ok',
            'status': 200,
            'content_type': 'application/json'
        })
        response = send_json_to_slack_channel({'text': 'Hello, Socnet'},
                                              'my_channel')
        self.assertEqual('ok', response[200])

    @responses.activate
    def testOpenForm(self):
        """
        Testing if open_form works
        """
        responses.add(**{
            'method': responses.POST,
            'url': slack_config['Views_Open_URL'],
            'body': 'ok',
            'status': 200,
            'content_type': 'application/json'
        })
        response = open_form('my_channel',
                             'my_tigger_id',
                             'test_data/slack/post_alert_form.json')
        self.assertEqual('ok', response[200])

    def testCreateAlertFromSlack(self):
        """
        Testing if create_alert_from_slack_message works
        """
        alert_json = create_alert_from_slack_message(post_alert_payload, TIME)
        self.assertEqual(sample_alert_json, alert_json)

    def testFormatAlert(self):
        """
        Testing if slack_format_alert works
        """
        ret = slack_format_alert([])
        self.assertEqual({'text':
                         'This alert does not exist or has been deleted.'},
                         ret)
        ret = slack_format_alert([(1,
                                   '2020-03-04 17:54:20',
                                   '10001',
                                   'New York City',
                                   'New York',
                                   'USA',
                                   'Fire',
                                   'Fire in the building',
                                   'High',
                                   'Socnet Tester')])
        self.assertEqual(sample_message, ret)

    def testUpdateAlert(self):
        """
        Testing if create_updated_alert_from_slack_message works
        """
        alert_json = create_updated_alert_from_slack_message(
            update_alert_payload,
            TIME,
            sample_alert_json)
        # update sample alert json
        sample_alert_json['event_zipcode'] = '10003'
        sample_alert_json['msg_sender'] = 'Slack'
        self.assertEqual(sample_alert_json, alert_json)
        # revert previous update for future use
        sample_alert_json['event_zipcode'] = '10001'
        sample_alert_json['msg_sender'] = 'NYU'

    def testGetAlertId(self):
        """
        Testing if get_id_from_payload works
        """
        payload = read_json('test_data/slack/update_alert_payload.json')
        alert_id = get_id_from_payload(payload)
        self.assertEqual('1', alert_id)

    def testConfirmation(self):
        """
        Testing if get_confirmation_form works
        """
        sample_message = read_json('test_data/slack/confirmation_message.json')
        response = get_confirmation_form('My Title', 'my message')
        self.assertEqual(sample_message, response)

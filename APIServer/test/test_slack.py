import unittest

import responses

from APIServer.commons import constants
from APIServer.commons.api_utils import read_json
from APIServer.slack.push import send_slack_log
from APIServer.slack.push import send_json_to_slack_channel
from APIServer.slack.push import open_form
from APIServer.slack.push import update_form
from APIServer.slack.format import get_confirmation_form
from APIServer.slack.format import slack_format_alert
from APIServer.slack.format import create_alert_from_slack_message
from APIServer.slack.format import create_updated_alert_from_slack_message
from APIServer.slack.format import get_id_from_payload
from APIServer.slack.format import get_filter_params_from_slack
from APIServer.slack.format import get_action_value
from APIServer.slack.format import get_page_value
from APIServer.slack.format import get_alerts_count


SLACK_CONFIG_PATH = \
    'APIServer/test_data/slack/test_slack.json'
SAMPLE_ALERT_JSON_PATH = \
    'APIServer/test_data/test_json.json'
POST_ALERT_PAYLOAD_PATH = \
    'APIServer/test_data/slack/post_alert_payload.json'
UPDATE_ALERT_PAYLOAD_PATH = \
    'APIServer/test_data/slack/update_alert_payload.json'
SAMPLE_MESSAGE_PATH = \
    'APIServer/test_data/slack/formatted_slack_message.json'
TIME = constants.TEST_TIME
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

    @responses.activate
    def testUpdateForm(self):
        """
        Testing if update_form works
        """
        responses.add(**{
            'method': responses.POST,
            'url': slack_config['Log_URL'],
            'body': 'ok',
            'status': 200,
            'content_type': 'application/json'
        })
        responses.add(**{
            'method': responses.POST,
            'url': slack_config['Views_Update_URL'],
            'body': 'ok',
            'status': 200,
            'content_type': 'application/json'
        })
        response = update_form('my_view_id',
                               'my_hash',
                               {})
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
                                   'Socnet Tester',
                                   'Active')])
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
        self.assertEqual(alert_json['zipcode'], '10003')
        self.assertEqual(alert_json['sender'], 'Slack')
        self.assertEqual(alert_json['active'], 'Not Active')

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

    def testGetFilterParams(self):
        """
        Testing if get_filter_params_from_slack works
        """
        payload = read_json('test_data/slack/filter_alerts_payload.json')
        response = get_filter_params_from_slack(payload)
        sample_response = {}
        sample_response['country'] = 'USA'
        sample_response['state'] = 'New York'
        sample_response['type'] = 'Fire'
        sample_response['severity'] = 'Low'
        sample_response['since_date'] = '2019-01-01'
        sample_response['limit'] = 5
        sample_response['active'] = 'y'
        self.assertEqual(sample_response, response)

    def testGetActionPageAndCount(self):
        """
        Testing if get_action_value, get_page_value, get_alerts_count works
        """
        payload = read_json('test_data/slack/next_page_payload.json')
        action = get_action_value(payload)
        page = get_page_value(payload)
        alerts_count = get_alerts_count(payload)
        self.assertEqual('next_page', action)
        self.assertEqual(1, page)
        self.assertEqual(10, alerts_count)

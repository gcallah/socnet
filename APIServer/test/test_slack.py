import unittest

import responses

from APIServer.commons.api_utils import read_json
from APIServer.slack.push import send_slack_log, send_json_to_slack
from APIServer.slack.format import create_alert_from_slack_message


test_config_path = 'test_data/test_slack.json'
sample_alert_json_path = 'test_data/test_json.json'
slack_config = read_json(test_config_path)
sample_alert_json = read_json(sample_alert_json_path)


class TestCase(unittest.TestCase):

    @responses.activate
    def testPush(self):
        """
        Testing whether send_slack_log and send_json_to_slack work
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
        response = send_json_to_slack('Hello, Socnet', slack_config['url'])
        self.assertEqual('ok', response[200])


    def testCreateAlertFromSlack(self):
        """
        Testing if create_alert_from_slack_message works
        """
        payload = slack_config['modal_submission_payload']
        time = '2019-11-01 17:45:32'
        alert_json = create_alert_from_slack_message(payload, time)
        self.assertEqual(sample_alert_json, alert_json)

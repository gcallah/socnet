import unittest

import responses

from APIServer.commons.api_utils import read_json
from APIServer.slack.push import push_to_slack, send_json_to_slack


test_config_path = 'test_data/test_slack.json'
slack_config = read_json(test_config_path)


class TestCase(unittest.TestCase):

    @responses.activate
    def testPush(self):
        """
        See if push_to_slack works.
        """
        responses.add(**{
            'method'         : responses.POST,
            'url'            : slack_config['url'],
            'body'           : 'ok',
            'status'         : 200,
            'content_type'   : 'application/json'
        })
        response = push_to_slack('Hello, Socnet')
        self.assertEqual('ok', response[200])
        response = send_json_to_slack('Hello, Socnet', slack_config['url'])
        self.assertEqual('ok', response[200])

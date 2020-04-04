import unittest

import responses

from APIServer.commons.api_utils import read_json
from APIServer.mattermost.push import push_to_mattermost

MATTERMOST_CONFIG_PATH = 'test_data/mattermost/test_mattermost.json'
MATTERMOST_TEST_CHANNEL = 'test'
mattermost_config = read_json(MATTERMOST_CONFIG_PATH
)
class TestMattermost(unittest.TestCase):

    @responses.activate
    def testPush(self):
        """
        Testing if push_to_mattermost works
        """
        responses.add(**{
            'method'         : responses.POST,
            'url'            : mattermost_config['Post_Chat_URL'],
            'body'           : 'ok',
            'status'         : 200,
            'content_type'   : 'application/json'
        })
        response = push_to_mattermost({'text': 'Hello, from Socnet'}, MATTERMOST_TEST_CHANNEL)
        self.assertEqual('ok', response[200])

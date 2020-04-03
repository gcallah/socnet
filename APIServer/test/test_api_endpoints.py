"""
"""
from unittest import TestCase, main
import json
import random
import os
import datetime
from flask_restplus import Resource, Api, fields
import responses

from APIServer import db

import APIServer.api_endpoints
from APIServer.api_endpoints import app, HelloWorld, MessageFormat, AlertsLists
from APIServer.commons.api_utils import err_return, read_json
from APIServer.alerts.operations import read_alert, update_alert, delete_alert
from APIServer.alerts.operations import read_all_alerts, write_alert
from APIServer.commons.form_api import validate_alert

test_config_path = 'test_data/test_config.json'
APIServer.api_endpoints.config = read_json(test_config_path)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"

SLACK_CONFIG_PATH = 'test_data/slack/test_slack.json'
slack_config = read_json(SLACK_CONFIG_PATH)


with app.app_context():
    db.session.remove()
    db.drop_all()

class Test(TestCase):
    def setUp(self):
        # none of the object's members names should have caps!
        self.messageformat = MessageFormat(Resource)
        self.HelloWorld = HelloWorld(Resource)
        self.alerts = AlertsLists(Resource)
        with app.app_context():
            db.create_all()
   
    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_hello_world(self):
        """
        See if HelloWorld works.
        """
        rv = self.HelloWorld.get()
        self.assertEqual(rv, {'hello': 'socnet'})

    def test_get_message_format(self):
        """
        See if MessageFormat returns the form.
        """
        rv = self.messageformat.get()
        print (rv)
        self.assertEqual(type(rv), dict) 

    def test_alerts(self):
        """
        See if alerts can be added, and called.
        """
        test_json = read_json('test_data/test_json.json')
        
        with app.test_client() as c:
            rv = c.get('/alerts')
            self.assertEqual(eval(rv.data.decode('utf-8')[:-1]), {})

            rv = c.post('/alerts', json=test_json)
            self.assertEqual(rv.status_code, 200)

            rv = c.get('/alerts')
            self.assertEqual(eval(rv.data.decode('utf-8')[:-1]), {'Alert 1':test_json})

    def test_err_return(self):
        """
        Testing whether we are able to get the right error message
        """
        rv = err_return("error message")
        self.assertEqual(rv, {"Error": "error message"})
        rv = read_json('makefile')
        self.assertEqual(rv, {"Error": "Not a valid json file"})
        rv = read_json('fake_file_location')
        self.assertEqual(rv, {"Error": "Json file not found"})


    def test_validate_alert(self):
        """
        Testing whether the validate alert function is correctly parsing
        """
        test_format = APIServer.api_endpoints.config['format_path']
        test_format = read_json(test_format)
        type_dict = APIServer.api_endpoints.config['format_dict']
        type_dict = read_json(type_dict)
        test_submission = {
                            "event_datetime": datetime.datetime.now(),
                            "event_type": "Fire",
                            "event_description": "A Fire",
                            "msg_sender": "Test"
                            }
        rv = validate_alert(test_format, type_dict, test_submission)
        self.assertEqual(rv[0], True)
        test_submission['event_description'] = 1
        rv = validate_alert(test_format, type_dict, test_submission)
        self.assertEqual(rv[0], False)
        test_submission['event_description'] = None
        rv = validate_alert(test_format, type_dict, test_submission)
        self.assertEqual(rv[0], False)
        test_submission['msg_sender'] = None
        rv = validate_alert(test_format, type_dict, test_submission)
        self.assertEqual(rv[0], False)


    def test_endpoints(self):
        """
        Testing whether or not the available endpoints show the right information
        """
        with app.test_client() as c:
            rv = c.get('/endpoints')
            endpoints = eval(rv.data.decode('utf-8')[:-1])['Available endpoints']
            self.assertEqual(type(endpoints), dict)
            for ep in endpoints:
                self.assertEqual(type(endpoints[ep]), dict)
                for method in endpoints[ep]:
                    self.assertEqual(type(endpoints[ep][method]), str)

    def test_alerts(self):
        """
        Testing whether or not the alerts module works
        """
        test_json = read_json('test_data/test_json.json')
        test_response = read_json('test_data/test_response.json')
        
        with app.test_client() as c:
            rv = c.get('/alerts')
            self.assertEqual(eval(rv.data.decode('utf-8')[:-1]), [])

            # Should not be able to update or delete alert before inserting
            rv = c.put('/alerts/1', json=test_json)
            self.assertEqual(rv.status_code, 404)

            rv = c.delete('/alerts/1')
            self.assertEqual(rv.status_code, 404)

            rv = c.post('/alerts', json=test_json)
            self.assertEqual(rv.status_code, 200)

            rv = c.put('/alerts/1', json=test_json)
            self.assertEqual(rv.status_code, 200)

            rv = c.get('/alerts/1')
            self.assertEqual(eval(rv.data.decode('utf-8')[:-1]), test_response)

            rv = c.delete('/alerts/1')
            self.assertEqual(rv.status_code, 200)

            rv = c.get('/alerts')
            self.assertEqual(eval(rv.data.decode('utf-8')[:-1]), [])

    def test_AlertFiltering(self):
        """
        Testing whether alerts filtering works
        """
        test_json = read_json('test_data/test_json.json')
        test_response = read_json('test_data/test_response.json')

        with app.test_client() as c:
            rv = c.get('/alerts')
            self.assertEqual(eval(rv.data.decode('utf-8')[:-1]), [])

            rv = c.post('/alerts', json=test_json)
            self.assertEqual(rv.status_code, 200)

            rv = c.get('/alerts?region=New York')
            self.assertEqual(eval(rv.data.decode('utf-8')[:-1]), test_response)

            rv = c.get('/alerts?region=New Jersey')
            self.assertEqual(eval(rv.data.decode('utf-8')[:-1]), [])

            rv = c.get('/alerts?severity=Low')
            self.assertEqual(eval(rv.data.decode('utf-8')[:-1]), test_response)

            rv = c.get('/alerts?severity=High')
            self.assertEqual(eval(rv.data.decode('utf-8')[:-1]), [])

            rv = c.get('/alerts?type=Fire')
            self.assertEqual(eval(rv.data.decode('utf-8')[:-1]), test_response)

            rv = c.get('/alerts?type=Smoke')
            self.assertEqual(eval(rv.data.decode('utf-8')[:-1]), [])

            rv = c.get('/alerts?date=2019-01-01')
            self.assertEqual(eval(rv.data.decode('utf-8')[:-1]), test_response)

            rv = c.get('/alerts?date=2022-01-01')
            self.assertEqual(eval(rv.data.decode('utf-8')[:-1]), [])

            rv = c.get('/alerts?country=USA')
            self.assertEqual(eval(rv.data.decode('utf-8')[:-1]), test_response)

            rv = c.get('/alerts?country=Canada')
            self.assertEqual(eval(rv.data.decode('utf-8')[:-1]), [])

            rv = c.get('/alerts?region=New York&severity=Low&type=Fire&country=USA&date=2019-01-01')
            self.assertEqual(eval(rv.data.decode('utf-8')[:-1]), test_response)

    def test_threads(self):
        """
        Testing whether or not the threads module works
        """
        test_json = read_json('test_data/test_json.json')
        test_threads_json = read_json('test_data/test_threads_json.json')

        with app.test_client() as c:

            rv = c.post('/alerts', json=test_json)
            rv = c.post('/alerts', json=test_json)

            rv = c.put('/threads/1', json={ 'text' : 'some comment'})
            self.assertEqual(rv.status_code, 200)

            rv = c.put('/threads/2', json={ 'text' : 'comment x'})
            self.assertEqual(rv.status_code, 200)

            rv = c.put('/threads/1', json={ 'text' : 'new comment'})
            self.assertEqual(rv.status_code, 200)

            rv = c.put('/threads/1', json={ 'text' : '3rd comment'})
            self.assertEqual(rv.status_code, 200)

            rv = c.put('/threads/2', json={ 'text' : 'comment yy'})
            self.assertEqual(rv.status_code, 200)

            rv = c.put('/threads/2', json={ 'text' : 'comment zzz'})
            self.assertEqual(rv.status_code, 200)

            rv = c.get('/threads/1')
            self.assertEqual(eval(rv.data.decode('utf-8')[:-1]), [{"1": "some comment"}, {"3": "new comment"}, {"4": "3rd comment"}])

            rv = c.delete('/alerts/1')
            # The thread associated with the alert should be deleted after the alert is deleted
            rv = c.get('/threads/1')
            self.assertEqual(rv.status_code, 404)

            rv = c.get('/threads/2')
            self.assertEqual(eval(rv.data.decode('utf-8')[:-1]), [{"2": "comment x"}, {"5": "comment yy"}, {"6": "comment zzz"}])

            rv = c.delete('/alerts/2')
            # The thread associated with the alert should be deleted after the alert is deleted
            rv = c.get('/threads/2')
            self.assertEqual(rv.status_code, 404)

       
    def test_threads_err(self):
        """
        Testing whether or not the threads module returns 404 code when a thread does not exist
        """
        with app.test_client() as c:

            rv = c.put('/threads/1', json={ 'text' : 'some comment'})
            self.assertEqual(rv.status_code, 404)

            rv = c.get('/threads/1')
            self.assertEqual(rv.status_code, 404)


    @responses.activate
    def test_slack(self):
        """
        Testing if Slack related endpoints work
        """
        responses.add(**{
            'method'         : responses.POST,
            'url'            : slack_config['Log_URL'],
            'body'           : 'ok',
            'status'         : 200,
            'content_type'   : 'application/json'
        })
        responses.add(**{
            'method'         : responses.POST,
            'url'            : slack_config['Post_Chat_URL'],
            'body'           : 'ok',
            'status'         : 200,
            'content_type'   : 'application/json'
        })
        responses.add(**{
            'method'         : responses.POST,
            'url'            : slack_config['Views_Open_URL'],
            'body'           : 'ok',
            'status'         : 200,
            'content_type'   : 'application/json'
        })
        with app.test_client() as c:
            # check if /slack/submit can handle the calls without payload 
            rv = c.post('/slack/submit')
            self.assertEqual(rv.status_code, 200)

            # check if /slack/post_alert works (it opens a form in Slack)
            rv = c.post('/slack/post_alert', data=dict(trigger_id='my_trigger_id', channel_id='my_channel'))
            self.assertEqual(rv.status_code, 200)

            # check if we can post an alert through /slack/submit 
            POST_PAYLOAD_PATH = APIServer.api_endpoints.config['slack_post_payload']
            post_alert_payload = read_json(POST_PAYLOAD_PATH)
            rv = c.post('/slack/submit', data=dict(payload=json.dumps(post_alert_payload)))
            self.assertEqual(rv.status_code, 200)

            # check if the previous alert was successfully posted
            rv = c.get('alerts/1')
            self.assertEqual(len(eval(rv.data.decode('utf-8')[:-1])), 1)

            # check if /slack/get_alert works
            rv = c.post('/slack/get_alert', data=dict(text='1', channel_id='my_channel'))
            self.assertEqual(rv.status_code, 200)

            # check if /slack/get_alerts works
            rv = c.post('/slack/get_alerts', data=dict(text='[1,2]', channel_id='my_channel'))
            self.assertEqual(rv.status_code, 200)

            # check if /slack/update_alert works (it opens a form in Slack)
            rv = c.post('/slack/update_alert', data=dict(trigger_id='my_trigger_id', channel_id='my_channel'))
            self.assertEqual(rv.status_code, 200)

            # check if we can update an alert through /slack/submit 
            UPDATE_PAYLOAD_PATH = APIServer.api_endpoints.config['slack_update_payload']
            update_alert_payload = read_json(UPDATE_PAYLOAD_PATH)
            rv = c.post('/slack/submit', data=dict(payload=json.dumps(update_alert_payload)))
            self.assertEqual(rv.status_code, 200)

            # try to use /slack/submit to update an alert that does not exist
            UPDATE_PAYLOAD_PATH = APIServer.api_endpoints.config['slack_update_payload_invalid']
            update_alert_payload = read_json(UPDATE_PAYLOAD_PATH)
            rv = c.post('/slack/submit', data=dict(payload=json.dumps(update_alert_payload)))
            self.assertEqual(rv.status_code, 200)

            # check if /slack/delete_alert works
            rv = c.post('/slack/delete_alert', data=dict(text='1'))
            self.assertEqual(rv.status_code, 200)

            # check if the previous alert was successfully deleted
            rv = c.get('alerts/1')
            self.assertEqual(len(eval(rv.data.decode('utf-8')[:-1])), 0)


if __name__ == "__main__":
    main()

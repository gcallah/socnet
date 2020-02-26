"""
"""
from unittest import TestCase, main, skip
import json
import random
import os
import datetime
from flask_restplus import Resource, Api, fields

import APIServer.api_endpoints
from APIServer.api_endpoints import app, HelloWorld, MessageFormat, AlertByCountry, AlertsLists
from APIServer.commons.api_utils import err_return, read_json
from APIServer.alerts.operations import read_alert, update_alert, delete_alert
from APIServer.alerts.operations import read_all_alerts, write_alert, read_alert_country
from APIServer.commons.form_api import validate_alert

from APIServer.database.sqlite import sqlite_init

test_config_path = 'test_data/test_config.json'
APIServer.api_endpoints.config = read_json(test_config_path)

class Test(TestCase):
    def setUp(self):
        # none of the object's members names should have caps!
        self.messageformat = MessageFormat(Resource)
        self.HelloWorld = HelloWorld(Resource)
        self.AlertByCountry = AlertByCountry(Resource)
        self.alerts = AlertsLists(Resource)

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

        test_db_dir = APIServer.api_endpoints.config['database_path']
        test_db_schema = APIServer.api_endpoints.config['table_schema_path']
        os.remove(test_db_dir)
        db_init(test_db_dir, test_db_schema)

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
        self.assertEqual(rv, {"Error:": "error message"})

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
        test_db_dir = APIServer.api_endpoints.config['database_path']
        test_db_schema = APIServer.api_endpoints.config['table_schema_path']
        sqlite_db_dir = test_db_dir+".db"
        if os.path.exists(sqlite_db_dir):
            os.remove(sqlite_db_dir)
        sqlite_init(test_db_dir, test_db_schema)
        test_json = read_json('test_data/test_json.json')
        test_response = read_json('test_data/test_response.json')
        
        with app.test_client() as c:
            rv = c.get('/alerts')
            self.assertEqual(eval(rv.data.decode('utf-8')[:-1]), [])

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

    def test_AlertByCountry(self):
        """
        Testing whether the filter by country endpoint works
        """

        test_db_dir = APIServer.api_endpoints.config['database_path']
        test_db_schema = APIServer.api_endpoints.config['table_schema_path']
        sqlite_db_dir = test_db_dir+".db"
        if os.path.exists(sqlite_db_dir):
            os.remove(sqlite_db_dir)
        sqlite_init(test_db_dir, test_db_schema)

        test_json = read_json('test_data/test_json.json')
        test_response = read_json('test_data/test_response.json')

        with app.test_client() as c:
            rv = c.get('/alerts')
            self.assertEqual(eval(rv.data.decode('utf-8')[:-1]), [])

            rv = c.post('/alerts', json=test_json)
            self.assertEqual(rv.status_code, 200)

            rv = c.get('/alerts/USA')
            self.assertEqual(eval(rv.data.decode('utf-8')[:-1]), test_response)
       
    def test_threads(self):
        """
        Testing whether or not the threads module works
        """
        test_db_dir = APIServer.api_endpoints.config['database_path']
        test_db_schema = APIServer.api_endpoints.config['table_schema_path']
        sqlite_db_dir = test_db_dir+".db"
        if os.path.exists(sqlite_db_dir):
            os.remove(sqlite_db_dir)
        sqlite_init(test_db_dir, test_db_schema)

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

            rv = c.get('/threads/2')
            self.assertEqual(eval(rv.data.decode('utf-8')[:-1]), [{"2": "comment x"}, {"5": "comment yy"}, {"6": "comment zzz"}])
       
    def test_threads_err(self):
        """
        Testing whether or not the threads module returns 404 code when a thread does not exist
        """
        test_db_dir = APIServer.api_endpoints.config['database_path']
        test_db_schema = APIServer.api_endpoints.config['table_schema_path']
        sqlite_db_dir = test_db_dir+".db"
        if os.path.exists(sqlite_db_dir):
            os.remove(sqlite_db_dir)
        sqlite_init(test_db_dir, test_db_schema)

        with app.test_client() as c:

            rv = c.put('/threads/1', json={ 'text' : 'some comment'})
            self.assertEqual(rv.status_code, 404)

            rv = c.get('/threads/1')
            self.assertEqual(rv.status_code, 404)

       
if __name__ == "__main__":
    main()

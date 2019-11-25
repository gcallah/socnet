"""
"""
from unittest import TestCase, main, skip
import json
import random
import os
from flask_restplus import Resource, Api, fields

import APIServer.api_endpoints
from APIServer.api_endpoints import app, HelloWorld, Alert, Alerts, MessageFormat, AlertByCountry
from APIServer.commons.api_utils import err_return, read_json
from APIServer.alerts.data_operations import write_alert, read_alert, db_init

from APIServer.database.sqlite import sqlite_init

test_config_path = 'test_data/test_config.json'
APIServer.api_endpoints.config = read_json(test_config_path)

class Test(TestCase):
    def setUp(self):
        # none of the object's members names should have caps!
        self.messageformat = MessageFormat(Resource)
        self.HelloWorld = HelloWorld(Resource)
        self.alert = Alert(Resource)
        self.alerts = Alerts(Resource)
        self.AlertByCountry = AlertByCountry(Resource)

    def test_hello_world(self):
        """
        See if HelloWorld works.
        """
        rv = self.HelloWorld.get()
        self.assertEqual(rv, {'hello': 'world'})

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

    def test_alert(self):
        """
        See if alert api works (uses id)
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

            test_json['event_type'] = 'Flood'

            rv = c.put('/alerts/1', json=test_json)
            self.assertEqual(rv.status_code, 200)

            rv = c.get('/alerts')
            self.assertEqual(eval(rv.data.decode('utf-8')[:-1]), {'Alert 1':test_json})

            rv = c.delete('/alerts/1')
            self.assertEqual(rv.status_code, 200)

            rv = c.get('/alerts')
            self.assertEqual(eval(rv.data.decode('utf-8')[:-1]), {})

        # Add full code here 

    def test_err_return(self):
        """
        Testing whether we are able to get the right error message
        """
        rv = err_return("error message")
        self.assertEqual(rv, {"Error:": "error message"})

    def test_endpoints(self):
        """
        Testing whether or not the available endpoints match
        """
        endpoints = ['/alerts', '/alerts/<int:id>', '/alerts/<string:country>', '/alerts_beta', '/endpoints', '/form', '/hello']

        with app.test_client() as c:
            rv = c.get('/endpoints')
            self.assertEqual(eval(rv.data.decode('utf-8')[:-1])['Available endpoints'], endpoints)

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
            rv = c.get('/alerts_beta')
            self.assertEqual(eval(rv.data.decode('utf-8')[:-1]), [])

            rv = c.post('/alerts_beta', json=test_json)
            self.assertEqual(rv.status_code, 200)

            rv = c.get('/alerts/USA')
            self.assertEqual(eval(rv.data.decode('utf-8')[:-1]), test_response)
       
if __name__ == "__main__":
    main()

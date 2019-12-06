"""
"""
from unittest import TestCase, main, skip
import json
import random
import os
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
        endpoints = ['/alerts', '/alerts/<int:id>', '/alerts/<string:country>', '/endpoints', '/form', '/hello', '/threads/<int:id>']

        with app.test_client() as c:
            rv = c.get('/endpoints')
            self.assertEqual(eval(rv.data.decode('utf-8')[:-1])['Available endpoints'], endpoints)

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
       
    def test_Threads(self):
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
        test_threads_json = read_json('test_data/test_threads_json.json')

        with app.test_client() as c:

            rv = c.post('/alerts', json=test_json)
            self.assertEqual(rv.status_code, 200)

            rv = c.put('/threads/1', json={ 'text' : 'some comment'})
            self.assertEqual(rv.status_code, 200)

            rv = c.get('/threads/1')
            self.assertEqual(eval(rv.data.decode('utf-8')[:-1]), [{"1": "some comment"}])

       
if __name__ == "__main__":
    main()

"""
"""
from unittest import TestCase, main, skip
import json
import random
from flask_restplus import Resource, Api, fields

from APIServer.api_endpoints import app, HelloWorld, Alert, Alerts, MessageFormat
from APIServer.api_utils import err_return
from APIServer.data_store import write_alert, read_alert, db_init

class Test(TestCase):
    def setUp(self):
        # none of the object's members names should have caps!
        self.messageformat = MessageFormat(Resource)
        self.HelloWorld = HelloWorld(Resource)
        self.alert = Alert(Resource)
        self.alerts = Alerts(Resource)

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
        self.assertEqual(type(rv), dict) 

    def test_alerts(self):
        """
        See if alerts can be added, and called.
        """

        test_db_dir = 'test_data/db_temp'
        db_init(test_db_dir)
        
        # Add full code here

    def test_alert(self):
        """
        See if alert api works (uses id)
        """

        test_db_dir = 'test_data/db_temp'
        db_init(test_db_dir)

        # Add full code here 

    def test_err_return(self):
        """
        Testing whether we are able to get the right error message
        """
        rv = err_return("error message")
        self.assertEqual(rv, {"Error:": "error message"})


if __name__ == "__main__":
    main()

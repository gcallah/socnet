# SOCNET API server
from flask import Flask, request
from flask_restplus import Resource, Api
from flask_cors import CORS
from form_api import get_form, get_fields
from data_store import db_init
from data_store import read_alert, update_alert
from data_store import read_all_alerts, write_new_alert
from api_utils import read_json

app = Flask(__name__)
CORS(app)
api = Api(app)

CONFIG_PATH = 'api_config.json'
config = read_json(CONFIG_PATH)
if config.get('Error:', None):
    config = read_json('APIServer/' + CONFIG_PATH)


@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


@api.route('/form')
class MessageFormat(Resource):
    def get(self):
        return get_form(config['format_path'])


resource_fields = api.model('Alert', get_fields())


@api.route('/alert/<int:id>')
class Alert(Resource):
    def get(self, id):
        """
        Get a specific alert with the given alert id
        """
        return read_alert(id)

    @api.doc(body=resource_fields)
    def put(self, id):
        """
        Update an alert in the system with the given alert id
        """
        return update_alert(request.json, id)


@api.route('/alert')
class Alerts(Resource):
    def get(self):
        """
        Get all alerts
        """
        return read_all_alerts()

    @api.doc(body=resource_fields)
    def put(self):
        """
        Put a new alert into the system
        """
        return write_new_alert(request.json)


if __name__ == '__main__':
    db_init()
    app.run(host=config['host'], port=config['port'], debug=config['debug'])

# SOCNET API server
from flask import Flask, request
from flask_restplus import Resource, Api
from flask_cors import CORS
from APIServer.commons.form_api import get_alert_form
from APIServer.commons.api_utils import read_json

from APIServer.database.sqlite import sqlite_init

from APIServer.alerts.operations import read_all_alerts
from APIServer.alerts.operations import write_alert
from APIServer.alerts.operations import read_alert
from APIServer.alerts.operations import update_alert
from APIServer.alerts.operations import delete_alert
from APIServer.alerts.operations import read_alert_country

app = Flask(__name__)
CORS(app)
api = Api(app, title='SOCNET API')

CONFIG_PATH = 'api_config.json'
config = read_json(CONFIG_PATH)
if config.get('Error:', None):
    config = read_json('APIServer/' + CONFIG_PATH)

app.config.SWAGGER_UI_DOC_EXPANSION = 'list'


@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        """
        A Hello World API for testing
        """
        return {'hello': 'world'}


@api.route('/endpoints')
class Endpoints(Resource):
    def get(self):
        """
        List our endpoints.
        """
        endpoints = sorted(rule.rule for rule in api.app.url_map.iter_rules())
        endpoints = list(filter(lambda x: not x.startswith('/swagger')
                                and not x.startswith('/static')
                                and not x == '/', endpoints))
        return {"Available endpoints": endpoints}


@api.route('/form')
class MessageFormat(Resource):
    def get(self):
        """
        Get the format of an alert
        """
        return get_alert_form(config['format_path'])


alert = api.schema_model('Alert', get_alert_form(config['format_path']))


@api.route('/alerts')
class AlertsLists(Resource):
    def get(self):
        """
        Get all alerts
        """
        return read_all_alerts(config['database_path'])

    @api.expect(alert)
    def post(self):
        """
        Put a new alert into the system
        """
        return write_alert(config['database_path'], request.json)


@api.route('/alerts/<int:id>')
class Alerts(Resource):
    def get(self, id):
        """
        Get a specific alert with the given alert id
        """
        return read_alert(config['database_path'], id)

    @api.expect(alert)
    def put(self, id):
        """
        Update an alert in the system with the given alert id
        """
        return update_alert(config['database_path'], request.json, id)

    def delete(self, id):
        """
        Delete an alert in the system with the given alert id
        """
        return delete_alert(config['database_path'], id)


@api.route('/alerts/<string:country>')
class AlertByCountry(Resource):
    def get(self, country):
        """
        Get all alerts for the given country
        """
        return read_alert_country(config['database_path'], country)


@api.route('/threads/<int:id>')
class Threads(Resource):
    def get(self, id):
        """
        List all comments under a thread(thread id is given)
        """
        return [], 200

    def put(self, id):
        """
        Post a new comment under a thread(thread id is given)
        """
        return {"message": "Successs"}, 200


if __name__ == '__main__':
    sqlite_init(config['database_path'], config['table_schema_path'])
    app.run(host=config['host'], port=config['port'], debug=config['debug'])

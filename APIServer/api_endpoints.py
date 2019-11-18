# SOCNET API server
from flask import Flask, request
from flask_restplus import Resource, Api
from flask_cors import CORS
from APIServer.form_api import get_form, get_fields
from APIServer.data_store import db_init
from APIServer.data_store import read_alert, update_alert, delete_alert
from APIServer.data_store import read_all_alerts, write_new_alert
from APIServer.api_utils import read_json

app = Flask(__name__)
CORS(app)
api = Api(app, title='SOCNET API')
app.config.SWAGGER_UI_DOC_EXPANSION = 'list'

CONFIG_PATH = 'api_config.json'
config = read_json(CONFIG_PATH)
if config.get('Error:', None):
    config = read_json('APIServer/' + CONFIG_PATH)


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
        return get_form(config['format_path'])


resource_fields = api.model('Alert', get_fields())


@api.route('/alert/<int:id>')
class Alert(Resource):
    def get(self, id):
        """
        Get a specific alert with the given alert id
        """
        return read_alert(config['database_path'], id)

    @api.doc(body=resource_fields)
    def put(self, id):
        """
        Update an alert in the system with the given alert id
        """
        return update_alert(config['database_path'], request.json, id)

    def delete(self, id):
        """
        Delete an alert in the system with the given alert id
        """
        return delete_alert(config['database_path'], request.json, id)


@api.route('/alert')
class Alerts(Resource):
    def get(self):
        """
        Get all alerts
        """
        return read_all_alerts(config['database_path'])

    @api.doc(body=resource_fields)
    def put(self):
        """
        Put a new alert into the system
        """
        return write_new_alert(config['database_path'], request.json)

if __name__ == '__main__':
    db_init(config['database_path'])
    app.run(host=config['host'], port=config['port'], debug=config['debug'])
# SOCNET API server
from flask import request
from APIServer import create_app
from flask_restplus import Resource, Api, fields
from APIServer.commons.form_api import get_alert_form
from APIServer.commons.api_utils import read_json
from APIServer.commons.endpoint_api import get_endpoints

from APIServer.database.sqlite import sqlite_init

from APIServer.alerts.operations import read_all_alerts
from APIServer.alerts.operations import write_alert
from APIServer.alerts.operations import read_alert
from APIServer.alerts.operations import update_alert
from APIServer.alerts.operations import delete_alert
from APIServer.alerts.operations import read_alert_country
from APIServer.alerts.operations import read_all_alerts_beta
from APIServer.alerts.operations import write_alert_beta
from APIServer.alerts.operations import update_alert_beta
from APIServer.alerts.operations import delete_alert_beta
from APIServer.alerts.operations import read_alert_beta
from APIServer.alerts.operations import read_alert_country_beta

from APIServer.threads.operations import get_comments
from APIServer.threads.operations import add_comment
from APIServer.threads.operations import add_comment_beta

from APIServer.slack.push import push_to_slack
from APIServer.slack.format import slack_format_alert

from APIServer.mattermost.push import push_to_mattermost

import json

CONFIG_PATH = 'api_config.json'
# config is a dictionary of configuration params:
config = read_json(CONFIG_PATH)
if config.get('Error:', None):
    config = read_json('APIServer/' + CONFIG_PATH)

app = create_app(config)

api = Api(app, title='SOCNET API')

app.config.SWAGGER_UI_DOC_EXPANSION = 'list'


@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        """
        A Hello World API for testing
        """
        return {'hello': 'socnet'}


@api.route('/test_pipeline')
class testPipeline(Resource):
    def get(self):
        """
        Test of pipeline
        """
        return {'test': 'reboot'}


@api.route('/endpoints')
class Endpoints(Resource):
    def get(self):
        """
        List our endpoints.
        """
        return get_endpoints(api, app)


@api.route('/alert_format')
class AlertFormat(Resource):
    def get(self):
        """
        Get the format of an alert
        """
        return get_alert_form(config['alert_format_path'])


@api.route('/form')
class MessageFormat(Resource):
    def get(self):
        """
        Get the format of an alert
        """
        return get_alert_form(config['format_path'])


alert = api.schema_model('Alert',
                         get_alert_form(config['format_path']))


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
@api.doc(params={'id': 'An Alert id number'})
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
@api.doc(params={'country': 'A country to retrieve all alerts from'})
class AlertByCountry(Resource):
    def get(self, country):
        """
        Get all alerts for the given country
        """
        return read_alert_country(config['database_path'], country)


comment = api.model('Comment', {'text': fields.String})


@api.route('/threads/<int:id>')
@api.doc(params={'id': 'An Alert id number'})
class Threads(Resource):
    def get(self, id):
        """
        List all comments under a thread(thread id is given)
        """
        return get_comments(config['database_path'], id)

    @api.expect(comment)
    def put(self, id):
        """
        Post a new comment under a thread(thread id is given)
        """
        return add_comment(config['database_path'], request.json, id)


@api.route('/threads_beta/<int:id>')
@api.doc(params={'id': 'An Alert id number'})
class ThreadsBeta(Resource):
    # def get(self, id):
    #     """
    #     List all comments under a thread(thread id is given)
    #     """
    #     return get_comments_beta(id)

    @api.expect(comment)
    def put(self, id):
        """
        Post a new comment under a thread(thread id is given)
        """
        return add_comment_beta(request.json, id)


@api.route('/alerts_beta')
class AlertsListsBeta(Resource):
    def get(self):
        """
        Get all alerts
        """
        return read_all_alerts_beta()

    @api.expect(alert)
    def post(self):
        """
        Put a new alert into the system
        """
        return write_alert_beta(request.json)


@api.route('/alerts_beta/<int:id>')
@api.doc(params={'id': 'An Alert id number'})
class AlertsBeta(Resource):
    def get(self, id):
        """
        Get a specific alert with the given alert id
        """
        return read_alert_beta(id)

    @api.expect(alert)
    def put(self, id):
        """
        Update an alert in the system with the given alert id
        """
        return update_alert_beta(request.json, id)

    def delete(self, id):
        """
        Delete an alert in the system with the given alert id
        """
        return delete_alert_beta(id)


@api.route('/alerts_beta/<string:country>')
@api.doc(params={'country': 'A country to retrieve all alerts from'})
class AlertByCountryBeta(Resource):
    def get(self, country):
        """
        Get all alerts for the given country
        """
        return read_alert_country_beta(country)


@api.route('/slack_alerts_beta')
class SlackAlertsBeta(Resource):
    def get(self):
        """
        Get all alerts and send it to Slack
        """
        text = read_all_alerts_beta()
        text = text.get_json()  # return a dictionary
        return push_to_slack(text)

    def post(self):
        """
        Put a new alert into the system through a Slack message
        """
        alert_json = json.loads(request.form['text'])
        return write_alert_beta(alert_json)


@api.route('/slack_alert_beta/<int:id>')
@api.doc(params={'id': 'An Alert id number'})
class SlackAlertBeta(Resource):
    def get(self, id):
        """
        Get a specific alert with the given alert id and send it to Slack
        """
        text = read_alert_beta(id)
        text = text.get_json()  # return a dictionary
        return push_to_slack(text)


@api.route('/slack_alerts')
class SlackAlerts(Resource):
    def get(self):
        """
        Get all alerts and send it to Slack
        """
        text = read_all_alerts(config['database_path'])
        return push_to_slack(text)

    def post(self):
        """
        Put a new alert into the system through a Slack message
        """
        alert_json = json.loads(request.form['text'])
        return write_alert(config['database_path'], alert_json)


@api.route('/slack_get_alert')
class SlackAlert(Resource):
    def post(self):
        """
        Get a specific alert with the given alert id and send it to Slack
        """
        alert_id = request.form['text']
        try:
            id = int(alert_id)
            text = read_alert(config['database_path'], id)
            formated_alert = slack_format_alert(text)
            return push_to_slack(formated_alert)
        except ValueError:
            ERROR_MESSAGE = 'Please input a valid alert id.'
            return push_to_slack(ERROR_MESSAGE)


@api.route('/slack_echo')
class SlackEcho(Resource):
    def post(self):
        """
        A test API for echoing back Slack messages
        """
        user = request.form['user_name']
        text = request.form['text']
        return push_to_slack(user + ' : ' + text)


@api.route('/mattermost_hello')
class MattermostHello(Resource):
    def post(self):
        """
        An API to send hello_world messages to Mattermost
        """
        text = 'HELLO_WORLD from API Server!'
        return push_to_mattermost(text)


@api.route('/mattermost_alert/<int:id>')
@api.doc(params={'id': 'An Alert id number'})
class MattermostAlert(Resource):
    def get(self, id):
        """
        Get alert with the given alert id and send it to mattermost
        """
        text = read_alert(config['database_path'], id)
        return push_to_mattermost(text)


@api.route('/mattermost_echo')
class MattermostEcho(Resource):
    def post(self):
        """
        A test API for echoing back Mattermost messages
        """
        user = request.form['user_name']
        text = request.form['text']
        return push_to_mattermost('msg sent.\ntext:' + text + '\nuser:' + user)


@api.route('/mattermost_alerts')
class MattermostAlerts(Resource):
    def get(self):
        """
        Get all alerts and send it to Mattermost
        """
        text = read_all_alerts(config['database_path'])
        return push_to_mattermost(text)

    def post(self):
        """
        Put a new alert into the system through a Mattermost message
        """
        alert_json = json.loads(request.form['text'])
        return write_alert(config['database_path'], alert_json)


if __name__ == '__main__':
    sqlite_init(config['database_path'], config['table_schema_path'])
    app.run(host=config['host'], port=config['port'], debug=config['debug'])

# SOCNET API server
from flask import request
from APIServer import create_app
from flask_restplus import Resource, Api, fields
from APIServer.commons.form_api import get_alert_form
from APIServer.commons.api_utils import read_json
from APIServer.commons.endpoint_api import get_endpoints

from APIServer.alerts.operations import read_filtered_alerts
from APIServer.alerts.operations import write_alert
from APIServer.alerts.operations import read_alert
from APIServer.alerts.operations import update_alert
from APIServer.alerts.operations import delete_alert
from APIServer.alerts.operations import number_of_alerts

from APIServer.threads.operations import get_comments
from APIServer.threads.operations import add_comment

from APIServer.slack.push import send_slack_log
from APIServer.slack.push import send_json_to_slack_channel
from APIServer.slack.push import open_form
from APIServer.slack.format import slack_format_alert
from APIServer.slack.operations import handle_interaction

from APIServer.mattermost.push import push_to_mattermost

from werkzeug.middleware.proxy_fix import ProxyFix

import os
import json

CONFIG_PATH = 'api_config.json'
# config is a dictionary of configuration params:
config = read_json(CONFIG_PATH)

port = int(os.environ.get("PORT", config['port']))

app = create_app(config)

# fix the bug that 'no api definition provided'
# when deployed to Heroku
app.wsgi_app = ProxyFix(app.wsgi_app)

api = Api(app, title='SOCNET API')

app.config.SWAGGER_UI_DOC_EXPANSION = 'list'


@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        """
        A Hello World API for testing
        """
        return {'hello': 'socnet'}


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


@api.route('/filters')
class FilterValues(Resource):
    def get(self):
        """
        Get the values to populate the filter form
        """
        return get_alert_form(config['filter_form_values_path'])


@api.route('/form')
class MessageFormat(Resource):
    def get(self):
        """
        Get the format of an alert
        """
        return get_alert_form(config['format_path'])


alert = api.schema_model('Alert',
                         get_alert_form(config['format_path']))


@api.route('/number_of_alerts')
class TotalAlerts(Resource):
    def get(self):
        """
        Get the total number of alerts
        """
        return number_of_alerts()


@api.route('/alerts')
class AlertsLists(Resource):
    @api.doc(params={'severity': 'Filter alerts by severity'})
    @api.doc(params={'date': 'Filter alerts by date'})
    @api.doc(params={'type': 'Filter alerts by type'})
    @api.doc(params={'region': 'Filter alerts by region'})
    @api.doc(params={'country': 'Filter alerts by country'})
    @api.doc(params={'active': 'Filter alerts by active status. \
        Enter y or n'})
    @api.doc(params={'limit': 'Pagination parameter. \
        Indicate the max number of results returned. \
        If not provided, the default value will be set to 100.'})
    @api.doc(params={'offset': 'Pagination parameter. \
        Indicate the offset of the first result. \
        If not provided, the default value will be set to 0.'})
    def get(self):
        """
        Get multiple (filtered) alerts based on the query parameters
        """
        return read_filtered_alerts(request.args)

    @api.expect(alert)
    def post(self):
        """
        Put a new alert into the system
        """
        return write_alert(request.json)


@api.route('/alerts/<int:id>')
@api.doc(params={'id': 'An Alert id number'})
class Alerts(Resource):
    def get(self, id):
        """
        Get a specific alert with the given alert id
        """
        return read_alert(id)

    @api.expect(alert)
    def put(self, id):
        """
        Update an alert in the system with the given alert id
        """
        return update_alert(request.json, id)

    def delete(self, id):
        """
        Delete an alert in the system with the given alert id
        """
        return delete_alert(id)


comment = api.model('Comment', {'text': fields.String})


@api.route('/threads/<int:id>')
@api.doc(params={'id': 'An Alert id number'})
class Threads(Resource):
    def get(self, id):
        """
        List all comments under a thread(thread id is given)
        """
        return get_comments(id)

    @api.expect(comment)
    def put(self, id):
        """
        Post a new comment under a thread(thread id is given)
        """
        return add_comment(request.json, id)


@api.route('/slack/post_alert')
class SlackPostAlert(Resource):
    def post(self):
        """
        Post a new alert into the system through a Slack message
        """
        send_slack_log('Entered /slack/post_alert')
        send_slack_log('Request info:')
        send_slack_log(str(request.form))
        trigger_id = request.form['trigger_id']
        channel_id = request.form['channel_id']
        response = open_form(channel_id,
                             trigger_id,
                             config['slack_post_form_path'])
        send_slack_log('Response info:')
        send_slack_log(str(response))
        return 'Please enter the new alert information in the form'


@api.route('/slack/get_alert')
class SlackGetAlert(Resource):
    def post(self):
        """
        Get a specific alert with the given alert id and send it to Slack
        """
        send_slack_log('Entered /slack/get_alert')
        send_slack_log('Request info:')
        send_slack_log(str(request.form))
        alert_id = request.form['text']
        channel_id = request.form['channel_id']
        try:
            id = int(alert_id)
        except ValueError:
            return "Invalid Alert ID: " + str(alert_id)
        text = read_alert(id)
        formated_alert = slack_format_alert(text)
        response = send_json_to_slack_channel(formated_alert, channel_id)
        send_slack_log('Response info:')
        send_slack_log(response)
        return "Alert " + str(id) + " fetched"


@api.route('/slack/update_alert')
class SlackUpdateAlert(Resource):
    def post(self):
        """
        Update an alert in the system through a Slack message
        """
        send_slack_log('Entered /slack/update_alert')
        send_slack_log('Request info:')
        send_slack_log(str(request.form))
        trigger_id = request.form['trigger_id']
        channel_id = request.form['channel_id']
        response = open_form(channel_id,
                             trigger_id,
                             config['slack_update_form_path'])
        send_slack_log('Response info:')
        send_slack_log(str(response))
        return 'Please enter the updated alert information in the form'


@api.route('/slack/delete_alert')
class SlackDeleteAlert(Resource):
    def post(self):
        """
        Delete an alert in the system through a Slack message
        """
        send_slack_log('Entered /slack/delete_alert')
        send_slack_log('Request info:')
        send_slack_log(str(request.form))
        alert_id = json.loads(request.form['text'])
        return delete_alert(int(alert_id))


@api.route('/slack/filter_alerts')
class SlacFilterAlerts(Resource):
    def post(self):
        """
        Filter alerts in the system through a Slack message
        """
        send_slack_log('Entered /slack/filter_alerts')
        send_slack_log('Request info:')
        send_slack_log(str(request.form))
        trigger_id = request.form['trigger_id']
        channel_id = request.form['channel_id']
        response = open_form(channel_id,
                             trigger_id,
                             config['slack_filter_form_path'])
        send_slack_log('Response info:')
        send_slack_log(str(response))
        return 'Please enter alerts filtering information in the form'


@api.route('/slack/submit')
class SlackSubmit(Resource):
    @api.doc(responses={200: 'OK'})
    def post(self):
        """
        An API that handles all Slack submit events(interactions)
        """
        send_slack_log('Entered /slack/submit')
        send_slack_log('Request info:')
        send_slack_log(str(request.form))
        if request.form.get('payload') is None:
            send_slack_log('Invalid request: no payload')
            return
        else:
            return handle_interaction(json.loads(request.form['payload']))


@api.route('/mattermost_hello')
class MattermostHello(Resource):
    def post(self):
        """
        An API to send hello_world messages to Mattermost
        """
        text = 'HELLO from socnet API Server!'
        return push_to_mattermost(text)


@api.route('/mattermost_alert')
class MattermostAlert(Resource):
    def post(self):
        """
        Get alert with the requested alert id and return to mattermost
        """
        try:
            alertId = int(request.form['text'])
        except ValueError:
            return {"text": "please enter a valid integer as alert Id."}
        alert = str(read_alert(alertId))
        return {"text": alert}


@api.route('/mattermost_echo')
class MattermostEcho(Resource):
    def post(self):
        """
        A test API for echoing back Mattermost messages
        """
        user = request.form['user_name']
        text = request.form['text']
        return {"text": 'msg sent successfully.\ntext:'
                + text + '\nuser:' + user}


@api.route('/mattermost_alerts')
class MattermostAlerts(Resource):
    def get(self):
        """
        Get all alerts and send it to Mattermost
        """
        text = read_filtered_alerts(request.args)
        return push_to_mattermost(text)

    def post(self):
        """
        Put a new alert into the system through a Mattermost message
        """
        try:
            alert_json = json.loads(request.form['text'])
        except json.decoder.JSONDecodeError:
            return {"text": "Failed to send alert. Incorrect json format."}
        alertId = write_alert(alert_json)
        responseText = 'successfully created alert ' \
                       'with id: ' + alertId
        return {"text": responseText}


if __name__ == '__main__':
    app.run(host=config['host'], port=port, debug=config['debug'])

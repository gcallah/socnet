# SOCNET API server
from flask import request
from APIServer import create_app
from flask_restplus import Resource, Api, fields
from APIServer.commons.form_api import get_alert_form
from APIServer.commons.form_api import create_alert_json
from APIServer.commons.api_utils import read_json
from APIServer.commons.endpoint_api import get_endpoints

from APIServer.alerts.operations import read_all_alerts
from APIServer.alerts.operations import read_filtered_alerts
from APIServer.alerts.operations import write_alert
from APIServer.alerts.operations import read_alert
from APIServer.alerts.operations import update_alert
from APIServer.alerts.operations import delete_alert
from APIServer.alerts.operations import read_alert_country

from APIServer.threads.operations import get_comments
from APIServer.threads.operations import add_comment

from APIServer.slack.push import send_slack_log
from APIServer.slack.push import send_json_to_slack_channel
from APIServer.slack.push import open_form
from APIServer.slack.format import slack_format_alert
from APIServer.slack.format import create_alert_from_slack_message
from APIServer.slack.format import create_updated_alert_from_slack_message
from APIServer.slack.format import get_id_from_payload

from APIServer.mattermost.push import push_to_mattermost

import json
import datetime

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
    @api.doc(params={'severity': 'Event severity'})
    @api.doc(params={'date': 'Event date'})
    @api.doc(params={'type': 'Event type'})
    @api.doc(params={'region': 'Event region'})
    def get(self):
        """
        Get all alerts or filtered alerts based on the query parameters
        """
        if request.args:
            return read_filtered_alerts(request.args)
        else:
            return read_all_alerts()

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


@api.route('/alerts/<string:country>')
@api.doc(params={'country': 'A country to retrieve all alerts from'})
class AlertByCountry(Resource):
    def get(self, country):
        """
        Get all alerts for the given country
        """
        return read_alert_country(country)


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


@api.route('/slack_post_alert')
class SlackPostAlert(Resource):
    def post(self):
        """
        Post a new alert into the system through a Slack message
        """
        send_slack_log('Entered /slack_post_alert ; Request info:')
        send_slack_log(str(request.form))
        trigger_id = request.form['trigger_id']
        channel_id = request.form['channel_id']
        response = open_form(channel_id,
                             trigger_id,
                             config['slack_post_form_path'])
        send_slack_log(str(response))
        return 'Please enter the alert information in the form'


@api.route('/slack_get_alert')
class SlackGetAlert(Resource):
    def post(self):
        """
        Get a specific alert with the given alert id and send it to Slack
        """
        send_slack_log('Entered /slack_get_alert ; Request info:')
        send_slack_log(str(request.form))
        alert_id = request.form['text']
        channel_id = request.form['channel_id']
        id = int(alert_id)
        text = read_alert(id)
        formated_alert = slack_format_alert(text)
        response = send_json_to_slack_channel(formated_alert, channel_id)
        send_slack_log(response)
        return "Alert " + str(id) + " fetched"


@api.route('/slack_update_alert')
class SlackUpdateAlert(Resource):
    def post(self):
        """
        Update an alert in the system through a Slack message
        """
        send_slack_log('Entered /slack_update_alert ; Request info:')
        send_slack_log(str(request.form))
        trigger_id = request.form['trigger_id']
        channel_id = request.form['channel_id']
        response = open_form(channel_id,
                             trigger_id,
                             config['slack_update_form_path'])
        send_slack_log(str(response))
        return 'Please enter new alert information in the form'


@api.route('/slack_delete_alert')
class SlackDeleteAlert(Resource):
    def post(self):
        """
        Delete an alert in the system through a Slack message
        """
        send_slack_log('Entered /slack_delete_alert ; Request info:')
        send_slack_log(str(request.form))
        alert_id = json.loads(request.form['text'])
        return delete_alert(int(alert_id))


@api.route('/slack_get_alerts')
class SlackGetAlerts(Resource):
    def post(self):
        """
        Get multiple alerts and send them to Slack
        """
        send_slack_log('Entered /slack_get_alerts ; Request info:')
        send_slack_log(str(request.form))
        alert_id_list = json.loads(request.form['text'])
        channel_id = request.form['channel_id']
        for alert_id in alert_id_list:
            id = int(alert_id)
            text = read_alert(id)
            send_slack_log('Alert ' + str(id) + ' response: ' + str(text))
            formated_alert = slack_format_alert(text)
            send_json_to_slack_channel(formated_alert, channel_id)
        return "Alerts fetched"


@api.route('/slack_submit')
class SlackSubmit(Resource):
    @api.doc(responses={200: 'OK'})
    def post(self):
        """
        An API that handles all Slack submit events(interactions)
        """
        send_slack_log('Entered /slack_submit ; Request info:')
        send_slack_log(str(request.form))
        if request.form.get('payload') is None:
            send_slack_log('Invalid request: no payload')
            return
        else:
            payload_json = json.loads(request.form['payload'])
            if payload_json['type'] is None:
                send_slack_log('Invalid request: no "type" in payload')
                return
            if payload_json['type'] == 'view_submission':
                time = datetime.datetime.now() \
                               .strftime('%Y-%m-%d %H:%M:%S')
                if payload_json['view']['callback_id'] == 'post_alert':
                    alert_json = create_alert_from_slack_message(payload_json,
                                                                 time)
                    send_slack_log('New alert json:' + str(alert_json))
                    response = write_alert(alert_json)
                    send_slack_log(response)
                    return {'response_action': 'clear'}
                elif payload_json['view']['callback_id'] == 'update_alert':
                    alert_id = get_id_from_payload(payload_json)
                    send_slack_log('Alert id:' + str(alert_id))
                    alert_json = create_alert_json(read_alert(alert_id)[0])
                    send_slack_log('Old alert json:' + str(alert_json))
                    alert_json = create_updated_alert_from_slack_message(
                        payload_json,
                        time,
                        alert_json)
                    send_slack_log('New alert json:' + str(alert_json))
                    response = update_alert(alert_json, alert_id)
                    send_slack_log(response)
                    return {'response_action': 'clear'}
                else:
                    send_slack_log('Unknown callback_id in view_submission')
                    return
            else:
                send_slack_log('No action needed for this interaction')
                return


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
        text = read_alert(id)
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
        text = read_all_alerts()
        return push_to_mattermost(text)

    def post(self):
        """
        Put a new alert into the system through a Mattermost message
        """
        alert_json = json.loads(request.form['text'])
        return write_alert(alert_json)


if __name__ == '__main__':
    app.run(host=config['host'], port=config['port'], debug=config['debug'])

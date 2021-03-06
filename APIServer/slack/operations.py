import datetime

from APIServer.slack.format import slack_format_alert
from APIServer.slack.format import create_alert_from_slack_message
from APIServer.slack.format import create_updated_alert_from_slack_message
from APIServer.slack.format import get_confirmation_form
from APIServer.slack.format import get_alerts_page_form
from APIServer.slack.format import get_id_from_payload
from APIServer.slack.format import get_filter_params_from_slack
from APIServer.slack.format import get_action_value
from APIServer.slack.format import get_page_value
from APIServer.slack.format import get_alerts_count
from APIServer.slack.push import send_slack_log
from APIServer.slack.push import update_form
from APIServer.alerts.operations import write_alert
from APIServer.alerts.operations import read_alert
from APIServer.alerts.operations import update_alert
from APIServer.alerts.operations import read_filtered_alerts
from APIServer.commons.api_utils import read_json
from APIServer.commons.form_api import create_alert_json
from APIServer.commons import constants


PAGE_LIMIT = constants.SLACK_PAGE_LIMIT
ALERT_LIST_TEMPLATE = 'slack/templates/alert_lists.json'


def create_alerts_page_view(params):
    alert_list = read_filtered_alerts(params)
    view = read_json(ALERT_LIST_TEMPLATE)
    for alert_json in alert_list:
        formated_alert = slack_format_alert([alert_json])
        for section in formated_alert['blocks']:
            view['blocks'].append(section)
    return view


def handle_interaction(payload_json):
    if payload_json['type'] == 'view_submission':
        send_slack_log('Payload type: view_submission')
        time = datetime.datetime.now() \
                       .strftime('%Y-%m-%d %H:%M:%S')
        if payload_json['view']['callback_id'] == 'post_alert':
            send_slack_log('callback_id: ' + 'post_alert')
            alert_json = create_alert_from_slack_message(payload_json,
                                                         time)
            send_slack_log('New alert json: ' + str(alert_json))
            response = write_alert(alert_json)
            send_slack_log('Response info: ')
            send_slack_log(response)
            return get_confirmation_form('Success', response)
        elif payload_json['view']['callback_id'] == 'update_alert':
            send_slack_log('callback_id: ' + 'update_alert')
            alert_id = get_id_from_payload(payload_json)
            send_slack_log('Alert id: ' + str(alert_id))
            ret = read_alert(alert_id)
            if len(ret) == 0:
                send_slack_log('Invalid Alert ID')
                return {'response_action': 'clear'}
            alert_json = create_alert_json(ret[0])
            send_slack_log('Old alert json: ' + str(alert_json))
            alert_json = create_updated_alert_from_slack_message(
                payload_json,
                time,
                alert_json)
            send_slack_log('New alert json: ' + str(alert_json))
            response = update_alert(alert_json, alert_id)
            send_slack_log('Response info: ')
            send_slack_log(response)
            return get_confirmation_form('Success', response)
        elif payload_json['view']['callback_id'] == 'filter_alerts':
            send_slack_log('callback_id: ' + 'filter_alerts')
            params = get_filter_params_from_slack(payload_json)
            view = create_alerts_page_view(params)
            return get_alerts_page_form(view)
        else:
            send_slack_log('Unknown callback_id in view_submission')
            return
    elif payload_json['type'] == 'block_actions':
        send_slack_log('Payload type: block_actions')
        action = get_action_value(payload_json)
        params = get_filter_params_from_slack(payload_json)
        page = get_page_value(payload_json)
        alerts_count = get_alerts_count(payload_json)
        if action == 'next_page':
            if alerts_count == PAGE_LIMIT:
                page = page + 1
        elif action == 'prev_page':
            if page > 1:
                page = page - 1
        else:
            send_slack_log('Invalid action')
            return
        params['offset'] = PAGE_LIMIT * (page - 1)
        send_slack_log('Parameters: ' + str(params))
        view = create_alerts_page_view(params)
        view['blocks'][1]['text']['text'] = \
            "*Showing page " + str(page) + " (max " + \
            str(PAGE_LIMIT) + " alerts per page)*"
        view_id = payload_json['view']['id']
        hash_value = payload_json['view']['hash']
        return update_form(view_id, hash_value, view)
    else:
        send_slack_log('No action needed for this interaction')
        return

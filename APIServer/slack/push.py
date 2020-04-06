import requests

from APIServer.commons.api_utils import read_json

SLACK_CONFIG_PATH = 'slack/slack_config.json'
slack_config = read_json(SLACK_CONFIG_PATH)


def send_slack_log(text):
    jsonToSend = {'text': str(text)}
    URL = slack_config['Log_Channel_Webhook']
    response = requests.post(URL, json=jsonToSend)
    return {response.status_code: response.text}


def send_json_to_slack_channel(jsonToSend, channel):
    URL = 'https://slack.com/api/chat.postMessage'
    jsonToSend['channel'] = channel
    headers = {"Authorization": slack_config['Bot_Access_Token'],
               "Content-Type": "application/json; charset=utf-8"}
    response = requests.post(URL, json=jsonToSend, headers=headers)
    return {response.status_code: response.text}


def open_form(channel, trigger_id, form_location):
    URL = 'https://slack.com/api/views.open'
    form = read_json(form_location)
    textToSend = {'channel': channel, 'trigger_id': trigger_id, 'view': form}
    headers = {"Authorization": slack_config['Bot_Access_Token'],
               "Content-Type": "application/json; charset=utf-8"}
    response = requests.post(URL, json=textToSend, headers=headers)
    return {response.status_code: response.text}


def get_confirmation_form(title, message):
    response_json = {}
    FORM_LOCATION = 'slack/confirmation.json'
    form = read_json(FORM_LOCATION)
    response_json['response_action'] = 'update'
    form['title']['text'] = title
    form['blocks'][0]['text']['text'] = message
    response_json['view'] = form
    return response_json

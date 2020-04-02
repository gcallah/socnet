from APIServer.commons.api_utils import read_json

import json

"""
Convert a raw alert (json) to a formatted message in Slack
"""
def slack_format_alert(alert_json):
	if alert_json == []:
		return {'text': 'This alert does not exist or has been deleted.'}

	MESSAGE_TEMPLATE = 'message.json'
	message = read_json(MESSAGE_TEMPLATE)
	if message.get('Error:', None):
		message = read_json('APIServer/slack/' + MESSAGE_TEMPLATE)
		if message.get('Error:', None):
			message = read_json('slack/' + MESSAGE_TEMPLATE)

	alert_id = alert_json[0][0]
	datetime = alert_json[0][1]
	location = alert_json[0][3] + ', ' \
			 + alert_json[0][4] + ', ' \
			 + alert_json[0][2] + ', ' \
			 + alert_json[0][5]
	event = alert_json[0][6]
	description = alert_json[0][7]
	severity = alert_json[0][8]
	sender = alert_json[0][9]
	THREAD_URL = 'https://gcallah.github.io/socnet/webapp.html#/thread/'
	url = THREAD_URL + str(alert_id)

	message['blocks'][1]['text']['text'] = '*' + event + '*\n' + description
	message['blocks'][2]['elements'][0]['text'] = location + '\n' \
												+ datetime + '\n' \
												+ severity + '\nby *' \
												+ sender + '*'
	message['blocks'][4]['accessory']['url'] = url
	return message


"""
Create a new raw alert (json) from the new alert form in Slack
"""
def create_alert_from_slack_message(payload, time):
	alert_json = {}
	values = payload['view']['state']['values']
	for value in values:
		for key in values[value]:
				if key == 'event_severity':
					alert_json[key] = values[value][key]['selected_option']['text']['text']
				else:
					alert_json[key] = values[value][key]['value']
	alert_json['event_datetime'] = time
	return alert_json


"""
Create an updated raw alert (json) from an update request in Slack
"""
def create_updated_alert_from_slack_message(payload, time, alert_json):
	values = payload['view']['state']['values']
	for value in values:
		for key in values[value]:
				if key == 'alert_id':
					continue
				if key == 'event_severity':
					if values[value][key].get('selected_option'):
						alert_json[key] = values[value][key]['selected_option']['text']['text']
				else:
					if values[value][key].get('value'):
						alert_json[key] = values[value][key]['value']
	alert_json['event_datetime'] = time
	return alert_json


"""
Get the alert id from an update request in Slack
"""
def get_id_from_payload(payload):
	values = payload['view']['state']['values']
	for value in values:
		for key in values[value]:
				if key == 'alert_id':
					alert_id = values[value][key]['value']
					return alert_id

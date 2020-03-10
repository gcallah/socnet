import json

def slack_format_alert(raw_alert):
	MESSAGE_TEMPLATE = '''
	{
		"blocks": [
			{
				"type": "divider"
			},
			{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": "*Event*\nDescription"
				}
			},
			{
				"type": "context",
				"elements": [
					{
						"type": "mrkdwn",
						"text": "Location\nDatetime\nSev\nby *wm1065*"
					}
				]
			},
	        
			{
				"type": "divider"
			},
			{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": "Go to Socnet to view this alert and its thread"
				},
				"accessory": {
						"type": "button",
						"text": {
							"type": "plain_text",
							"text": "Go to Socnet"
						},
						"style": "primary",
						"url": "https://gcallah.github.io/socnet/webapp.html#/thread/40"
					}
			},
			{
				"type": "divider"
			}
		]
	}
	'''
	message = json.loads(MESSAGE_TEMPLATE)

	alert_id = raw_alert[0][0]
	datetime = raw_alert[0][1]
	location = raw_alert[0][3] + ',' + raw_alert[0][2] + ',' + raw_alert[0][4]
	event = raw_alert[0][6]
	description = raw_alert[0][7]
	severity = raw_alert[0][8]
	sender = raw_alert[0][9]
	url = 'https://gcallah.github.io/socnet/webapp.html#/thread/' + str(alert_id)

	message['blocks'][1]['text']['text'] = '*' + event + '*\n' + description
	message['blocks'][2]['elements']['text'] = location + '\n' + datetime + '\n' + severity + '\nby *' + sender + '*'
	message['blocks'][4]['accessory']['url'] = url
	return message
import requests


def push_to_slack(text):
	textToSend = text
	URL = 'https://hooks.slack.com/services/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'
	response = requests.post(URL, json=textToSend)
	return { response.status_code : response.text }


def push_to_channel(channel, trigger_id):
	URL = 'https://slack.com/api/views.open'
	with open('dialog.json', 'r') as json_file:
		data=myfile.read()
	dialog = json.loads(data)
	textToSend = {'channel': channel, 'view': dialog}
	headers = {"Authorization": "Bearer xoxp-765850805047-790629649378-989309639635-00bf54bba4048c8414ad0983f630c586"}
	response = requests.post(URL, data=textToSend, headers=headers)
	return { response.status_code : response.text }

import requests


def push_to_slack(text):
	textToSend = {'text' : str(text)}
	url = 'https://hooks.slack.com/services/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'
	response = requests.post(url, json=textToSend)
	return { response.status_code : response.text }
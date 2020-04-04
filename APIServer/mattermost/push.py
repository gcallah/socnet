import requests


def push_to_mattermost(text, channel = None):
	jsonToSend = {'text' : str(text)}
	if channel != None:
		jsonToSend['channel'] = channel
	URL = 'http://18.235.204.147:8065/hooks/dse96wr583gwjesxbx48ykuy6r'
	response = requests.post(URL, json=jsonToSend)
	return { response.status_code : response.text }
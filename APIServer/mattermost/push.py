import requests


def push_to_mattermost(text):
	textToSend = {'text' : str(text)}
	URL = 'http://18.235.204.147:8065/hooks/dse96wr583gwjesxbx48ykuy6r'
	response = requests.post(URL, json=textToSend)
	return { response.status_code : response.text }
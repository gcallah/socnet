import requests


def push_to_mattermost(text):
	textToSend = {'text' : str(text)}
	URL = 'https://35727a1c.ngrok.io/hooks/oikmiyshk7na7j6xrq59eoze9w'
	response = requests.post(URL, json=textToSend)
	return { response.status_code : response.text }
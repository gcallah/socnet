import json
from APIServer.api_utils import err_return

def get_form(form_dir):
	try:
		with open(form_dir) as jfile:
			mess_form = json.loads(jfile)
		return mess_form
	except FileNotFoundError:
		return err_return("Message format file not found")


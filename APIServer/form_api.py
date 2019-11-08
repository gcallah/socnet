import json
from APIServer.api_utils import err_return


def get_form():
    try:
        with open('./alert_props.json', 'r') as jfile:
            mess_form = json.load(jfile)
        return mess_form
    except FileNotFoundError:
        return err_return("Message format file not found")

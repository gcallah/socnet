from api_utils import read_json


def get_form(path):
    return read_json(path + '/alert_props.json')

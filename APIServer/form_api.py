from api_utils import read_json
from flask_restplus import fields


def get_form(path):
    return read_json(path + '/alert_props.json')

def get_model():
    return {
        'date': fields.DateTime,
        'event_loc': fields.String,
        'event_type': fields.String,
        'event_description': fields.String,
        'event_severity': fields.String,
        'msg_sender': fields.String
    }
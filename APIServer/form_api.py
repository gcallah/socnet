from flask_restplus import fields
from APIServer.api_utils import read_json


def get_form(path):
    return read_json(path)


def get_fields():
    return {
        'date': fields.DateTime,
        'event_loc': fields.String,
        'event_type': fields.String,
        'event_description': fields.String,
        'event_severity': fields.String,
        'msg_sender': fields.String
    }

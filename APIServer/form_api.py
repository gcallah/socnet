from flask_restplus import fields
from APIServer.api_utils import read_json
from datetime import datetime


def get_form(path):
    return read_json(path)


def get_fields():
    return {
        'date': fields.DateTime(
            example=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ),
        'event_loc': fields.String,
        'event_type': fields.String,
        'event_description': fields.String,
        'event_severity': fields.String,
        'msg_sender': fields.String
    }

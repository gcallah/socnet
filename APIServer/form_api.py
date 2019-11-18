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
        'event_loc': fields.String(
            example='Some location'
        ),
        'event_type': fields.String(
            example='Some type'
        ),
        'event_description': fields.String(
            example='Some description'
        ),
        'event_severity': fields.String(
            example='Low'
        ),
        'msg_sender': fields.String(
            example='Sender\'s name'
        )
    }

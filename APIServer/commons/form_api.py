from flask_restplus import fields
from APIServer.commons.api_utils import read_json
from datetime import datetime


def get_alert_fields(path):
    return read_json(path).get('properties')


def get_alert_form(path):
    return read_json(path)

import os
import sqlite3
from APIServer.commons.api_utils import read_json, write_json, delete_json

from APIServer.commons.form_api import create_alerts, create_alert
from APIServer.database.sqlite import get_db


def write_alert_legacy(path, alert, id):
    if read_alert_legacy(path, id) == 'No record found!':
        write_json(path, 'Alert ' + str(id), alert)
        return_msg = 'Put alert ' + str(id) + ' into DB... Success!'
    else:
        return_msg = 'Alert ' + str(id) + ' already exists!'
    return return_msg


def update_alert_legacy(path, alert, id):
    if read_alert_legacy(path, id) == 'No record found!':
        return_msg = 'Can not update. '
        return_msg += 'Alert ' + str(id) + ' does not exist.'
    else:
        delete_json(path, 'Alert ' + str(id))
        write_json(path, 'Alert ' + str(id), alert)
        return_msg = 'Alert ' + str(id) + ' updated!'
    return return_msg


def delete_alert_legacy(path, alert, id):
    if read_alert_legacy(path, id) == 'No record found!':
        return_msg = 'Can not delete. '
        return_msg += 'Alert ' + str(id) + ' does not exist.'
    else:
        delete_json(path, 'Alert ' + str(id))
        return_msg = 'Alert ' + str(id) + ' deleted!'
    return return_msg


def read_alert_legacy(path, id):
    all_alerts = read_json(path)
    for alert in all_alerts:
        if alert == 'Alert ' + str(id):
            return {alert: all_alerts[alert]}
    return 'No record found!'


def get_alert_id(path):
    MAX_ALERT_ID = 65536
    for id in range(1, MAX_ALERT_ID):
        if read_alert_legacy(path, id) == 'No record found!':
            return id
    return 0


def write_new_alert_legacy(path, alert):
    id = get_alert_id(path)
    return write_alert_legacy(path, alert, id)


def read_all_alerts_legacy(path):
    return read_json(path)


def db_init(path, schema):
    # sqlite_init(path, schema)
    if not os.path.isfile(path):
        f = open(path, 'w+')
        f.write('{}')
        f.close()



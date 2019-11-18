import os
import sqlite3
from APIServer.api_utils import read_json, write_json, delete_json


def write_alert(path, alert, id):
    if read_alert(path, id) == 'No record found!':
        write_json(path, 'Alert ' + str(id), alert)
        return_msg = 'Put alert ' + str(id) + ' into DB... Success!'
    else:
        return_msg = 'Alert ' + str(id) + ' already exists!'
    return return_msg


def update_alert(path, alert, id):
    if read_alert(path, id) == 'No record found!':
        return_msg = 'Can not update. '
        return_msg += 'Alert ' + str(id) + ' does not exist.'
    else:
        delete_json(path, 'Alert ' + str(id))
        write_json(path, 'Alert ' + str(id), alert)
        return_msg = 'Alert ' + str(id) + ' updated!'
    return return_msg


def delete_alert(path, alert, id):
    if read_alert(path, id) == 'No record found!':
        return_msg = 'Can not delete. '
        return_msg += 'Alert ' + str(id) + ' does not exist.'
    else:
        delete_json(path, 'Alert ' + str(id))
        return_msg = 'Alert ' + str(id) + ' deleted!'
    return return_msg


def read_alert(path, id):
    all_alerts = read_json(path)
    for alert in all_alerts:
        if alert == 'Alert ' + str(id):
            return {alert: all_alerts[alert]}
    return 'No record found!'


def get_alert_id(path):
    MAX_ALERT_ID = 65536
    for id in range(1, MAX_ALERT_ID):
        if read_alert(path, id) == 'No record found!':
            return id
    return 0


def write_new_alert(path, alert):
    id = get_alert_id(path)
    return write_alert(path, alert, id)

def read_all_alerts(path):
    return read_json(path)


def db_init(path):
    sqlite_init(get_sqlite_path(path))
    if not os.path.isfile(path):
        f = open(path, 'w+')
        f.write('{}')
        f.close()

def get_sqlite_path(path):
    return path+'.db'

def get_db(path):
    return sqlite3.connect(path)

def sqlite_init(path):
    sqlite3.connect(path)
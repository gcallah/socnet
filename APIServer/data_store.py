import os
from api_utils import read_json, write_json


CONFIG_PATH = 'api_config.json'
config = read_json(CONFIG_PATH)
DB = config['database_path']


def write_alert(alert, id):
    if read_alert(id) == 'No record found!':
        write_json(DB, 'Alert ' + str(id), alert)
        return_msg = 'Put key ' + str(id) + ' into DB... Success!'
    else:
        return_msg = 'Key ' + str(id) + ' already exists!'
    return return_msg


def read_alert(id):
    all_alerts = read_json(DB)
    for alert in all_alerts:
        if alert == 'Alert ' + str(id):
            return {alert: all_alerts[alert]}
    return 'No record found!'


def get_alert_id():
    MAX_ALERT_ID = 65536
    for id in range(1, MAX_ALERT_ID):
        if read_alert(id) == 'No record found!':
            return id
    return 0


def write_new_alert(alert):
    id = get_alert_id()
    return write_alert(alert, id)


def read_all_alerts():
    return read_json(DB)


def db_init():
    if not os.path.isfile(DB):
        f = open(DB, 'w+')
        f.write('{}')
        f.close()

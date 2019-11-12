import os
from api_utils import read_json


CONFIG_PATH = 'api_config.json'
config = read_json(CONFIG_PATH)
DB = config['database_path']


def get_msg_str(msg, key):
    msg_str = ('Record '
               + str(key) + ' : '
               + 'Date '
               + msg.get('date', '')
               + ' | '
               + 'Location '
               + msg.get('event_loc', '')
               + ' | '
               + 'Type '
               + msg.get('event_type', '')
               + ' | '
               + 'Description '
               + msg.get('event_description', '')
               + ' | '
               + 'Severity '
               + msg.get('event_severity', '')
               + ' | '
               + 'Sender '
               + msg.get('msg_sender', '')
               + '\n')
    return msg_str


def write_alert(msg, key):
    if read_alert(key) == 'No record found!':
        f = open(DB, 'a')
        msg_str = get_msg_str(msg, key)
        f.write(msg_str)
        f.close()
        return_msg = 'Put key ' + str(key) + ' into DB... Success!'
    else:
        return_msg = 'Key ' + str(key) + ' already exists!'
    return return_msg


def read_alert(key):
    f = open(DB, 'r')
    for line in f:
        num = line.split(' ')[1]
        if int(num) == key:
            return line
    return 'No record found!'


def db_init():
    if not os.path.isfile(DB):
        open(DB, 'w+')

import os
import sqlite3
from APIServer.commons.api_utils import read_json, write_json, delete_json

from APIServer.commons.form_api import create_alerts, create_alert
from APIServer.database.sqlite import get_db


def read_all_alerts(path):
    conn = get_db(path)
    cur = conn.cursor()
    cur.execute("SELECT * FROM alert")
    return create_alerts(cur.fetchall())


def write_alert(path, alert):
    event_zipcode = alert['event_loc']['event_zipcode']
    event_city = alert['event_loc']['event_city']
    event_state = alert['event_loc']['event_state']
    event_country = alert['event_loc']['event_country']
    event_description = alert['event_description']
    msg_sender = alert['msg_sender']
    event_datetime = alert['event_datetime']
    severity = alert['event_severity']

    columns = '(event_zipcode, event_city, event_state, event_country, event_description, sender, event_date, severity)'    
    values = '(\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\')' % \
                (event_zipcode, event_city, event_state, event_country, event_description, msg_sender, event_datetime, severity)
    
    conn = get_db(path)
    cur = conn.cursor()
    cur.execute("INSERT INTO alert " + columns +" VALUES " + values)
    conn.commit()
    conn.close()  
    return 

def update_alert(path, alert):
    event_zipcode = alert['event_loc']['event_zipcode']
    event_city = alert['event_loc']['event_city']
    event_state = alert['event_loc']['event_state']
    event_country = alert['event_loc']['event_country']
    event_description = alert['event_description']
    msg_sender = alert['msg_sender']
    event_datetime = alert['event_datetime']
    severity = alert['event_severity']

    columns = '(event_zipcode, event_city, event_state, event_country, event_description, sender, event_date, severity)'    
    values = '(\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\')' % \
                (event_zipcode, event_city, event_state, event_country, event_description, msg_sender, event_datetime, severity)
    
    conn = get_db(path)
    cur = conn.cursor()
    cur.execute("INSERT INTO alert " + columns +" VALUES " + values)
    conn.commit()
    conn.close()  
    return 

def read_alert(path, alert):
    event_zipcode = alert['event_loc']['event_zipcode']
    event_city = alert['event_loc']['event_city']
    event_state = alert['event_loc']['event_state']
    event_country = alert['event_loc']['event_country']
    event_description = alert['event_description']
    msg_sender = alert['msg_sender']
    event_datetime = alert['event_datetime']
    severity = alert['event_severity']

    columns = '(event_zipcode, event_city, event_state, event_country, event_description, sender, event_date, severity)'    
    values = '(\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\')' % \
                (event_zipcode, event_city, event_state, event_country, event_description, msg_sender, event_datetime, severity)
    
    conn = get_db(path)
    cur = conn.cursor()
    cur.execute("INSERT INTO alert " + columns +" VALUES " + values)
    conn.commit()
    conn.close()  
    return 

def delete_alert(path, alert):
    event_zipcode = alert['event_loc']['event_zipcode']
    event_city = alert['event_loc']['event_city']
    event_state = alert['event_loc']['event_state']
    event_country = alert['event_loc']['event_country']
    event_description = alert['event_description']
    msg_sender = alert['msg_sender']
    event_datetime = alert['event_datetime']
    severity = alert['event_severity']

    columns = '(event_zipcode, event_city, event_state, event_country, event_description, sender, event_date, severity)'    
    values = '(\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\')' % \
                (event_zipcode, event_city, event_state, event_country, event_description, msg_sender, event_datetime, severity)
    
    conn = get_db(path)
    cur = conn.cursor()
    cur.execute("INSERT INTO alert " + columns +" VALUES " + values)
    conn.commit()
    conn.close()  
    return 


def read_alert_country(path, country):
    conn = get_db(path)
    cur = conn.cursor()
    cur.execute('SELECT * FROM alert WHERE event_country = \'%s\'' % (country))
    return create_alerts(cur.fetchall())

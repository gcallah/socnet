from APIServer.commons.form_api import create_alerts
from APIServer.database.sqlite import get_db
from APIServer.database.models import Alert,Thread,Comment
from APIServer.database.schema import AlertSchema
from APIServer import db
from flask import jsonify

def read_all_alerts(path):
    conn = get_db(path)
    cur = conn.cursor()
    cur.execute("SELECT * FROM alert")
    return create_alerts(cur.fetchall())

def dic_lst_to_tuple_lst(dic_lst):
    final_lst = []
    for dic in dic_lst:
        tup = (dic["id"],dic["event_datetime"],dic["event_zipcode"],dic["event_city"],dic["event_state"],dic["event_country"],dic["event_type"],dic["event_description"],dic["event_severity"],dic["msg_sender"])
        final_lst.append(tup)
    return final_lst


def read_all_alerts_beta():
    alerts = Alert.query.all()
    alert_schema = AlertSchema(many=True)
    alerts_json = alert_schema.dump(alerts)
    return dic_lst_to_tuple_lst(alerts_json)
    # print(type(alerts_json))
    # print(alerts_json[0])
    # # print('alerts_json: ', alerts_json)
    # return jsonify({'alerts:' : alerts_json})


def write_alert(path, alert):
    event_zipcode = alert['event_zipcode']
    event_city = alert['event_city']
    event_state = alert['event_state']
    event_country = alert['event_country']
    event_type = alert['event_type']
    event_description = alert['event_description']
    msg_sender = alert['msg_sender']
    event_datetime = alert['event_datetime']
    event_severity = alert['event_severity']

    columns = '(event_zipcode, event_city, event_state, event_country, event_type, event_description, msg_sender, event_datetime, event_severity)'
    values = '(\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\')' % \
                (event_zipcode, event_city, event_state, event_country, event_type, event_description, msg_sender, event_datetime, event_severity)

    conn = get_db(path)
    cur = conn.cursor()
    cur.execute("INSERT INTO alert " + columns +" VALUES " + values)
    alert_id = cur.lastrowid
    cur.execute('INSERT INTO thread (id, first_comment_id, last_comment_id) VALUES (%d, %d, %d)' % (alert_id, -1, -1))
    conn.commit()
    conn.close()
    return 'Alert ' + str(alert_id) + ' inserted'


def write_alert_beta(alert):
    new_alert = Alert(event_zipcode = alert['event_zipcode'],
    event_city = alert['event_city'],
    event_state = alert['event_state'],
    event_country = alert['event_country'],
    event_type = alert['event_type'],
    event_description = alert['event_description'],
    msg_sender = alert['msg_sender'],
    event_datetime = alert['event_datetime'],
    event_severity = alert['event_severity'])
    db.session.add(new_alert)
    db.session.commit()
    new_thread = Thread(id=new_alert.id,first_comment_id=-1,last_comment_id=-1)
    db.session.add(new_thread)
    db.session.commit()
    return 'Alert ' + str(new_alert.id) + ' inserted'

def update_alert(path, alert, id):
    event_zipcode = alert['event_zipcode']
    event_city = alert['event_city']
    event_state = alert['event_state']
    event_country = alert['event_country']
    event_type = alert['event_type']
    event_description = alert['event_description']
    msg_sender = alert['msg_sender']
    event_datetime = alert['event_datetime']
    event_severity = alert['event_severity']

    columns = '(id, event_zipcode, event_city, event_state, event_country, event_type, event_description, msg_sender, event_datetime, event_severity)'
    values = '(\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\')' % \
                (id, event_zipcode, event_city, event_state, event_country, event_type, event_description, msg_sender, event_datetime, event_severity)

    conn = get_db(path)
    cur = conn.cursor()
    cur.execute('DELETE FROM alert WHERE id = \'%d\'' % (id))
    cur.execute("INSERT INTO alert " + columns +" VALUES " + values)
    conn.commit()
    conn.close()  
    return 

def update_alert_beta(alert, id):
    fetched_alert = Alert.query.get(id)
    if fetched_alert is None:
        return 'Alert ' + str(id) + ' not exist'
    fetched_alert.event_zipcode = alert['event_zipcode']
    fetched_alert.event_city = alert['event_city']
    fetched_alert.event_state = alert['event_state']
    fetched_alert.event_country = alert['event_country']
    fetched_alert.event_type = alert['event_type']
    fetched_alert.event_description = alert['event_description']
    fetched_alert.msg_sender = alert['msg_sender']
    fetched_alert.event_datetime = alert['event_datetime']
    fetched_alert.event_severity = alert['event_severity']
    db.session.commit()
    return


def read_alert(path, id):
    conn = get_db(path)
    cur = conn.cursor()
    cur.execute('SELECT * FROM alert WHERE id = \'%d\'' % (id))
    return create_alerts(cur.fetchall())

def read_alert_beta(id):
    fetched_alert = Alert.query.get(id)
    alert_schema = AlertSchema()
    alert_json = alert_schema.dump(fetched_alert)
    print('alert_json: ', alert_json)
    return jsonify({'alert:' : alert_json})



def delete_alert(path, id):
    conn = get_db(path)
    cur = conn.cursor()
    cur.execute('DELETE FROM alert WHERE id = \'%d\'' % (id))
    conn.commit()
    conn.close()  
    return 

def delete_alert_beta(id):
    # when an alert is deleted, so does its thread and all comments?
    alert = Alert.query.get(id)
    if alert == None:
        return 'Alert ' + str(id) + ' not exist'
    db.session.delete(alert)
    db.session.commit()


def read_alert_country(path, country):
    conn = get_db(path)
    cur = conn.cursor()
    cur.execute('SELECT * FROM alert WHERE event_country = \'%s\'' % (country))
    return create_alerts(cur.fetchall())

def read_alert_country_beta(country):
    alerts = Alert.query.filter_by(event_country=country).all()
    alert_schema = AlertSchema(many=True)
    alerts_json = alert_schema.dump(alerts)
    print('alerts_json: ', alerts_json)
    return jsonify({'alerts:' : alerts_json})

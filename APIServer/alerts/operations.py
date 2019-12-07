from APIServer.commons.form_api import create_alerts
from APIServer.database.sqlite import get_db
from APIServer.database.models import Alert
from APIServer.database.schema import AlertSchema
from APIServer import db
from flask import jsonify

def read_all_alerts(path):
    conn = get_db(path)
    cur = conn.cursor()
    cur.execute("SELECT * FROM alert")
    return create_alerts(cur.fetchall())


def read_all_alerts_beta():
    alerts = Alert.query.all()
    alert_schema = AlertSchema(many=True)
    alerts_json = alert_schema.dump(alerts)
    print('alerts_json: ', alerts_json)
    return jsonify({'alerts:' : alerts_json})


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
    conn.commit()
    conn.close()
    return


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


def read_alert(path, id):
    conn = get_db(path)
    cur = conn.cursor()
    cur.execute('SELECT * FROM alert WHERE id = \'%d\'' % (id))
    return create_alerts(cur.fetchall())


def delete_alert(path, id):
    conn = get_db(path)
    cur = conn.cursor()
    cur.execute('DELETE FROM alert WHERE id = \'%d\'' % (id))
    conn.commit()
    conn.close()  
    return 


def read_alert_country(path, country):
    conn = get_db(path)
    cur = conn.cursor()
    cur.execute('SELECT * FROM alert WHERE event_country = \'%s\'' % (country))
    return create_alerts(cur.fetchall())

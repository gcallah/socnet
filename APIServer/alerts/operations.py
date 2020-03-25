from APIServer.commons.form_api import create_alerts
from APIServer.database.sqlite import get_db
from APIServer.database.models import Alert,Thread,Comment
from APIServer.database.schema import AlertSchema
from APIServer import db
from flask import jsonify

# return a list of dict
def convert_to_dic_list(obj):
    if type(obj) is list:
        # if list contain MarshalResut object
        if (len(obj)>0) and (type(obj[0]) is not dict):
            return [obj.data]
        else:
            return obj
    # if obj is a MarshalResult
    else:
        return obj.data
def dic_lst_to_tuple_lst(obj):
    dic_lst = convert_to_dic_list(obj)
    final_lst = []
    for dic in dic_lst:
        tup = (dic["id"],dic["event_datetime"],dic["event_zipcode"],dic["event_city"],dic["event_state"],dic["event_country"],dic["event_type"],dic["event_description"],dic["event_severity"],dic["msg_sender"])
        final_lst.append(tup)
    return final_lst


def read_all_alerts():
    alerts = Alert.query.all()
    alert_schema = AlertSchema(many=True)
    alerts_json = alert_schema.dump(alerts)
    return dic_lst_to_tuple_lst(alerts_json)


def write_alert(alert):
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


def update_alert(alert, id):
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
    return 'Alert ' + str(id) + ' updated'


def read_alert(id):
    fetched_alert = Alert.query.get(id)
    alert_schema = AlertSchema()
    alert_json = alert_schema.dump(fetched_alert)
    return dic_lst_to_tuple_lst([alert_json])



def delete_alert(id):
    # when an alert is deleted, so does its thread and all comments?
    alert = Alert.query.get(id)
    if alert == None:
        return 'Alert ' + str(id) + ' not exist'
    db.session.delete(alert)
    db.session.commit()
    return 'Alert ' + str(id) + ' deleted'


def read_alert_country(country):
    alerts = Alert.query.filter_by(event_country=country).all()
    alert_schema = AlertSchema(many=True)
    alerts_json = alert_schema.dump(alerts)
    return dic_lst_to_tuple_lst(alerts_json)

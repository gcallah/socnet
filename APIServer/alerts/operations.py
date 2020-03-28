from APIServer.database.models import Alert, Thread
from APIServer.database.schema import AlertSchema
from APIServer import db
from APIServer.threads.operations import delete_thread

from dateutil.parser import parse


# return a list of dict
def convert_to_dic_list(obj):
    if type(obj) is list:
        # if list contain MarshalResut object
        if (len(obj) > 0) and (type(obj[0]) is not dict):
            return [obj[0].data]
        else:
            return obj
    # if obj is a MarshalResult
    else:
        return obj.data


def dic_lst_to_tuple_lst(obj):
    dic_lst = convert_to_dic_list(obj)
    final_lst = []
    for dic in dic_lst:
        if dic == {}:
            continue
        tup = (dic["id"],
               dic["event_datetime"],
               dic["event_zipcode"],
               dic["event_city"],
               dic["event_state"],
               dic["event_country"],
               dic["event_type"],
               dic["event_description"],
               dic["event_severity"],
               dic["msg_sender"])
        final_lst.append(tup)
    return final_lst

def query_params_to_list(query_string):
    # query_string = query_string[1:-1]
    query_list = [ elem.strip() for elem in query_string.split(",")]
    return query_list

def read_all_alerts():
    alerts = Alert.query.all()
    alert_schema = AlertSchema(many=True)
    alerts_json = alert_schema.dump(alerts)
    return dic_lst_to_tuple_lst(alerts_json)


def write_alert(alert):
    """
    Add a new alert to database
    """
    new_alert = Alert(event_zipcode=alert['event_zipcode'],
                      event_city=alert['event_city'],
                      event_state=alert['event_state'],
                      event_country=alert['event_country'],
                      event_type=alert['event_type'],
                      event_description=alert['event_description'],
                      msg_sender=alert['msg_sender'],
                      event_datetime=alert['event_datetime'],
                      event_severity=alert['event_severity'])
    db.session.add(new_alert)
    db.session.commit()
    # add a new thread for the alert
    new_thread = Thread(id=new_alert.id,
                        first_comment_id=-1,
                        last_comment_id=-1)
    db.session.add(new_thread)
    db.session.commit()
    return 'Alert ' + str(new_alert.id) + ' inserted'


def update_alert(alert, id):
    fetched_alert = Alert.query.get(id)
    if fetched_alert is None:
        return {'message' : 'Alert ' + str(id) + ' does not exist'}, 404
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
    """
    delete an alert and associated thread from the database
    """
    alert = Alert.query.get(id)
    if alert is None:
        return {'message' : 'Alert ' + str(id) + ' does not exist'}, 404
    # delete associated thread
    delete_thread(id)
    # delete alert
    db.session.delete(alert)
    db.session.commit()
    return 'Alert ' + str(id) + ' deleted'


def read_alert_country(country):
    alerts = Alert.query.filter_by(event_country=country).all()
    alert_schema = AlertSchema(many=True)
    alerts_json = alert_schema.dump(alerts)
    return dic_lst_to_tuple_lst(alerts_json)


def read_filtered_alerts(query_params):
    print(query_params)
    severity_value = query_params.get('severity')
    date_value = query_params.get('date')
    type_value = query_params.get('type')
    region_value = query_params.get('region')
    alerts = None

    if region_value:
        required_regions = query_params_to_list(region_value)
        # print(required_regions)
        if alerts:
            alerts = Alert.query.filter(
                Alert.event_state.in_(required_regions))
        else:
            alerts = Alert.query.filter(
                Alert.event_state.in_(required_regions))
    
    if severity_value: 
        required_severity = query_params_to_list(severity_value)
        # print(required_severity)
        if alerts:
            alerts = alerts.filter(Alert.event_severity.in_(required_severity))
        else:
            alerts = Alert.query.filter(
                Alert.event_severity.in_(required_severity))

    if date_value:
        # parse date input in any format (MM-DD-YYY, DD-MM-YYYY, MM/DD/YYYY...)
        required_datetime = parse(date_value, fuzzy=True)
        # print(required_datetime)
        if alerts:
            alerts = alerts.filter(
                Alert.event_datetime >= required_datetime)
        else:
            alerts = Alert.query.filter(
                Alert.event_datetime >= required_datetime)
    
    if type_value:
        required_type = query_params_to_list(type_value)
        # print(required_type)
        if alerts:
            alerts = alerts.filter(
                Alert.event_type.in_(required_type))
        else:
            alerts = Alert.query.filter(
                Alert.event_type.in_(required_type))

    # alerts = alerts.all()
    # print(alerts)
    alert_schema = AlertSchema(many=True)
    alerts_json = alert_schema.dump(alerts)
    # print(dic_lst_to_tuple_lst(alerts_json))
    return dic_lst_to_tuple_lst(alerts_json)

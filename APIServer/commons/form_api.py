from APIServer.commons.api_utils import read_json


def get_alert_form(path):
    return read_json(path)


def create_alert_json(alert_tuple):
    '''
    Create alert_json from an alert tuple
    '''
    alert_json = {}
    alert_json['event_datetime'] = alert_tuple[1]
    alert_json['event_zipcode'] = alert_tuple[2]
    alert_json['event_city'] = alert_tuple[3]
    alert_json['event_state'] = alert_tuple[4]
    alert_json['event_country'] = alert_tuple[5]
    alert_json['event_type'] = alert_tuple[6]
    alert_json['event_description'] = alert_tuple[7]
    alert_json['event_severity'] = alert_tuple[8]
    alert_json['msg_sender'] = alert_tuple[9]
    return alert_json

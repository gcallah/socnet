from APIServer.commons.api_utils import read_json


def get_alert_form(path):
    return read_json(path)


def create_alert_json(alert_tuple):
    '''
    Create alert_json from an alert tuple
    '''
    alert_json = {}
    alert_json['datetime'] = alert_tuple[1]
    alert_json['zipcode'] = alert_tuple[2]
    alert_json['city'] = alert_tuple[3]
    alert_json['state'] = alert_tuple[4]
    alert_json['country'] = alert_tuple[5]
    alert_json['type'] = alert_tuple[6]
    alert_json['description'] = alert_tuple[7]
    alert_json['severity'] = alert_tuple[8]
    alert_json['sender'] = alert_tuple[9]
    return alert_json

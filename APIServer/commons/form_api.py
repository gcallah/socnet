from APIServer.commons.api_utils import read_json


def get_alert_form(path):
    return read_json(path)


def create_alert(db_record):
    if db_record is None:
        return None
    else:
        alert = db_record
        return alert


def create_alerts(db_records):
    '''
    Create alerts from db records
    '''
    alerts = []
    for record in db_records:
        alert = create_alert(record)
        alerts.append(alert)
    return alerts


def validate_alert(alert_format, alert):
    """
    Validate that the alert has the correct format
    """

    required = alert_format['required']
    for r in required:
        test = alert.get(r, None)
        if test is None:
            return False, 'Missing {}'.format(r)

        req_type = alert_format['properties'][r]['type']
        given_type = type(test)
        if req_type == 'string' and given_type != str:
            return False, '{} not given as string'.format(r)
        elif req_type == 'int' and given_type != int:
            return False, '{} not given as int'.format(r)
        else:
            pass
            # Object Type

    return True, ''

from APIServer.commons.api_utils import read_json
import datetime


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

    def test_prop(prop, submitted):
        type_dict = {}
        req_type = prop.get('type', None)
        if req_type is not None:
            if submitted is not None:
                pass
            else:
                return False, 'Missing entry of type {}'.format(req_type)
        else:
            return True, 'Nothing required'
            

    required = alert_format.get('required', None)
    if required is not None:
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

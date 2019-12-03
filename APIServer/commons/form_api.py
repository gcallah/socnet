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


def validate_alert(alert_format, type_dict, alert):
    """
    Validate that the alert has the correct format
    """

    def test_prop(prop, submitted):
        req_type = prop.get('type', None)
        if req_type is not None:
            if submitted is not None:
                convert_type = type_dict[req_type]
                if isinstance(submitted, eval(convert_type)):
                    return True, ''
                else:
                    return False, 'Not the appropriate type {}'.format(req_type)
            else:
                return False, 'Missing entry of type {}'.format(req_type)
        else:
            return True, 'Nothing required'

    def test_all_prop(all_prop, given):
        for p in all_prop.keys():
            check, mess = test_prop(all_prop[p], given.get(p, None))
            if check is False:
                return False, mess
        return True, ''
            
    required = alert_format.get('required', None)
    if required is not None:
        properties = alert_format.get('properties', None)
        for r in required:
            test = alert.get(r, None)
            if test is None:
                return False, 'Missing {}'.format(r)
            else:
                check, mess = test_prop(properties[r], test)
                if check is False:
                    return False, mess
        check, mess = test_all_prop(properties, alert)
        if check is False:
            return False, mess

    else:
        check, mess = test_all_prop(alert_format, alert)
        if check is False:
            return False, mess

    return True, ''

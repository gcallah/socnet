from APIServer.commons.api_utils import read_json


def get_alert_form(path):
    return read_json(path)


def create_alert(db_record):
	alert = db_record
	print (alert)
	return db_record


def create_alerts(db_records):
	'''
	Create alerts from db records
	'''
	alerts = []
	for record in db_records:
		alert = create_alert(record)
		alerts.append(alert)
	print (alerts)
	return alerts

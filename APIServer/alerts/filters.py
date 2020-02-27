# from APIServer.commons.form_api import create_alerts
# from APIServer.database.sqlite import get_db
# from APIServer.database.models import Alert
# from APIServer.database.schema import AlertSchema
# from APIServer import db
# from flask import jsonify

# def generate_query_string(filters):
#     # trial run
#     return "SELECT * FROM alerts WHERE event_state = 'Michigan'"


# def read_filtered_alerts(path, filters):
#     conn = get_db(path)
#     cur = conn.cursor()
#     QUERY = generate_query_string(filters)
#     cur.execute(QUERY)
#     return create_alerts(cur.fetchall())

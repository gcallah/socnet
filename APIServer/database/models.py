from APIServer import db
 
class Alert(db.Model):
    __tablename__ = "alerts"
 
    id = db.Column(db.Integer, primary_key=True)
    event_datetime = db.Column(db.Text)
    event_zipcode = db.Column(db.Text)
    event_city = db.Column(db.Text)
    event_state = db.Column(db.Text)
    event_country = db.Column(db.Text)
    event_type = db.Column(db.Text)
    event_description = db.Column(db.Text)
    event_severity = db.Column(db.Text)
    msg_sender = db.Column(db.Text)
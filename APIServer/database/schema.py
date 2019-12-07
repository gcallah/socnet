from APIServer import ma
from APIServer.database.models import Alert

class AlertSchema(ma.ModelSchema):
    class Meta:
        model = Alert
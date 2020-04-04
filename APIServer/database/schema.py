from APIServer import ma
from APIServer.database.models import Alert, Thread, Comment


class AlertSchema(ma.ModelSchema):
    class Meta:
        model = Alert


class ThreadSchema(ma.ModelSchema):
    class Meta:
        model = Thread


class CommentSchema(ma.ModelSchema):
    class Meta:
        model = Comment

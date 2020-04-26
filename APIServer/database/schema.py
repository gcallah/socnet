from APIServer.database.models import Alert, Thread, Comment
from marshmallow_sqlalchemy import ModelSchema


class AlertSchema(ModelSchema):
    class Meta:
        model = Alert


class ThreadSchema(ModelSchema):
    class Meta:
        model = Thread


class CommentSchema(ModelSchema):
    class Meta:
        model = Comment

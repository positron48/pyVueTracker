from marshmallow_sqlalchemy import ModelSchema
from backend.src.model import HashTag,Project


class ProjectSchema(ModelSchema):
    class Meta(object):
        model = Project

class HashTagSchema(ModelSchema):
    class Meta(object):
        model = HashTag

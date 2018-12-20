from marshmallow_sqlalchemy import ModelSchema
from backend.src.model import HashTag


class HashTagSchema(ModelSchema):
    class Meta:
        model = HashTag
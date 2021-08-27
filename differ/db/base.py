from .connection import connection
from peewee import Model


class BaseModel(Model):
    class Meta:
        database = connection

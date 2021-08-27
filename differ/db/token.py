import secrets

from .base import BaseModel
from peewee import CharField


class Token(BaseModel):
    user = CharField(unique=True)
    value = CharField(default=lambda: secrets.token_urlsafe(32), index=True, unique=True)

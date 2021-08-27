from .connection import connection
from .token import Token

connection.create_tables([Token])

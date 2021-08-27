from differ.constants import DATABASE_URL

from playhouse import db_url

connection = db_url.connect(DATABASE_URL)

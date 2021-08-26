from time import time

from differ.constants import CACHE_CONFIG, REDIS_CONNECTION

from flask import Flask
from flask_caching import Cache
from flask_session import Session


app = Flask(__name__)
app.config["SESSION_TYPE"] = "redis"
app.config["SESSION_REDIS"] = REDIS_CONNECTION

cache = Cache(app, config=CACHE_CONFIG)
Session(app)


@cache.memoize(timeout=5)
def funcall():
    return time()


@app.route("/")
def index():
    return str(funcall())

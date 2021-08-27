from differ.constants import CACHE_CONFIG

from flask import Flask
from flask_caching import Cache


app = Flask(__name__)
cache = Cache(app, config=CACHE_CONFIG)

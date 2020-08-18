import logging

import flask_login
from flask import Flask
from flask_cors import CORS

from Environment import Environment
from infracheck.Persistence import Persistence

# Log
log = logging.getLogger()
formatter = logging.Formatter('%(levelname)-8s %(asctime)s    %(message)-38s  %(name)s', "%Y-%m-%d %H:%M:%S")

# Stream Log
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
log.setLevel(Environment.LOG_LEVEL)
log.addHandler(stream_handler)

# File Log
file_handler = logging.FileHandler('debug.log')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)
log.addHandler(file_handler)

# Init Flask
app = Flask(__name__, static_url_path='')
app.secret_key = 'secret'
CORS(app)

login_manager = flask_login.LoginManager()

login_manager.init_app(app)
persistence_service = Persistence()

import infracheck.routes

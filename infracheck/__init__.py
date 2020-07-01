import logging

import flask_login
from flask import Flask

from Environment import Environment
from infracheck.Persistence import Persistence

log = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(levelname)-8s %(asctime)s    %(message)-38s  %(name)s', "%Y-%m-%d %H:%M:%S")
handler.setFormatter(formatter)
log.addHandler(handler)
log.setLevel(Environment.LOG_LEVEL)

app = Flask(__name__)
app.secret_key = 'secret'

login_manager = flask_login.LoginManager()

login_manager.init_app(app)
persistence_service = Persistence()

import infracheck.routes

import logging

import flask_login
from flask import Flask

from Environment import Environment
from infracheck.Persistence import Persistence

log = logging.getLogger(__name__)

logging.basicConfig(
    level=Environment.LOG_LEVEL,
    format="%(message)s     | %(asctime)s | %(name)s | %(levelname)s |",
    datefmt="%Y-%m-%d %H:%M:%S")
app = Flask(__name__)
app.secret_key = 'secret'

login_manager = flask_login.LoginManager()

login_manager.init_app(app)
persistence_service = Persistence()

import infracheck.routes

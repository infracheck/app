import flask_login
from flask import Flask

from infracheck.Persistence import Persistence

app = Flask(__name__)
app.secret_key = 'secret'

login_manager = flask_login.LoginManager()

login_manager.init_app(app)
persistence_service = Persistence()

import infracheck.routes

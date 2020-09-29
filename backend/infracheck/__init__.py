import logging

from flask import Flask
from flask_basicauth import BasicAuth
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy

# Log
log = logging.getLogger()
formatter = logging.Formatter('%(levelname)-8s %(asctime)s    %(message)-38s  %(name)s', "%Y-%m-%d %H:%M:%S")

# Init Flask
app = Flask(__name__, static_url_path='')

if app.env == "production":
    app.config.from_object('Configuration.ProductionConfig')
elif app.env == "development":
    app.config.from_object('Configuration.DevelopmentConfig')
else:
    app.config.from_object('Configuration.Config')

CORS(app)
basic_auth = BasicAuth(app)
jwt = JWTManager(app)

db = SQLAlchemy(app)
api = Api(app,
          title='InfraCheck - Backend',
          description="""
            This tool delivers you a universal codeless test server. 
            Send simple json files to InfraCheck and start complex test flows.
            Custom _plugins_ and _modules_ extend the functionality of this tool. """
          )

# Stream Log
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
log.setLevel(app.config['LOG_LEVEL'])
log.addHandler(stream_handler)

import infracheck.Api

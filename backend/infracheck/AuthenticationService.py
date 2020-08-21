import logging

from flask_basicauth import BasicAuth

from Environment import Environment
from infracheck import app

log = logging.getLogger()


def setup_basic_auth():
    if Environment.PRODUCTION:
        app.config['BASIC_AUTH_REALM'] = """Access to InfraCheck only allowed via BasicAuth. Please contact your 
        system administrator """
        app.config['BASIC_AUTH_USERNAME'] = Environment.USERNAME
        app.config['BASIC_AUTH_PASSWORD'] = Environment.PASSWORD
        app.config['BASIC_AUTH_FORCE'] = True
        BasicAuth(app)
        log.info(F"BasicAuth activated: Username: '{Environment.USERNAME}', Password: '{Environment.PASSWORD}'")
    else:
        log.info("BasicAuth deactivated")

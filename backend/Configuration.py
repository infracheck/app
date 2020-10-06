import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

"""
The following configuration can be configured:
PASSWORD   - Password for /login
SECURE     - Boolean indicates whether /login is required to use the API
"""


class Config(object):
    """Basic configuration"""
    ROOT_DIR = ROOT_DIR
    DEBUG = False
    TESTING = False

    SQLALCHEMY_DATABASE_URI = F"sqlite:///{ROOT_DIR}/infracheck.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    RESULT_FOLDER = F'{ROOT_DIR}/results/'

    SECURE_API = False
    JWT_SECRET_KEY = os.urandom(24).hex()
    PASSWORD = os.environ.get('PASSWORD') or "password"


class DevelopmentConfig(Config):
    """
    Config used for development purpose
    """
    DEBUG = True
    TESTING = True
    LOG_LEVEL = 'DEBUG'


class ProductionConfig(Config):
    LOG_LEVEL = 'WARN'
    SECURE_API = os.environ.get('SECURE') or False

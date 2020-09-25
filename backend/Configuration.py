import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class Config(object):
    """Basic configuration"""
    ROOT_DIR = ROOT_DIR
    DEBUG = False
    TESTING = False

    SQLALCHEMY_DATABASE_URI = F"sqlite:///{ROOT_DIR}/infracheck.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    BASIC_AUTH_FORCE = False
    RESULT_FOLDER = F'{ROOT_DIR}/results/'
    SECRET_KEY = "secret"


class DevelopmentConfig(Config):
    """
    Config used for development purpose
    """
    DEBUG = True
    TESTING = True
    LOG_LEVEL = 'DEBUG'


class ProductionConfig(Config):
    LOG_LEVEL = 'WARN'
    SECRET_KEY = os.environ.get('SECRET_KEY') or "secret"

    BASIC_AUTH_FORCE = True
    BASIC_AUTH_REALM = """Access to InfraCheck only allowed via BasicAuth. Please contact your system administrator """
    BASIC_AUTH_USERNAME = os.environ.get('AUTH_USERNAME') or "user"
    BASIC_AUTH_PASSWORD = os.environ.get('AUTH_PASSWORD') or "password"

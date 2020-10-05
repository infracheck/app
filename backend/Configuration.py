import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class Config(object):
    """Basic configuration"""
    ROOT_DIR = ROOT_DIR
    DEBUG = False
    TESTING = False

    SQLALCHEMY_DATABASE_URI = F"sqlite:///{ROOT_DIR}/infracheck.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    RESULT_FOLDER = F'{ROOT_DIR}/results/'
    SECRET_KEY = "secret"

    SECURE_API = False
    JWT_SECRET_KEY = "ROFL"
    AUTH_PASSWORD = os.environ.get('AUTH_PASSWORD') or "password"


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
    SECURE_API = True

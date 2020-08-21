import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Environment(object):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

    # Those can be changed
    LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'DEBUG'
    RESULT_FOLDER = os.environ.get('RESULT_FOLDER') or 'results/'
    DATABASE = F"{ROOT_DIR}/database.db"
    PRODUCTION = bool(os.environ.get('PRODUCTION')) or False
    USERNAME = os.environ.get('USER') or "user"
    PASSWORD = os.environ.get('PASSWORD') or "password"

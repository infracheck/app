import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Environment(object):
    ENV_VAR = os.environ.get('ENV_VAR') or 'DEFAULT'
    LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'DEBUG'

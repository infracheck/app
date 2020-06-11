import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    ENV_VAR = os.environ.get('ENV_VAR') or 'DEFAULT'

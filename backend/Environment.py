import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Environment(object):
    ENV_VAR = os.environ.get('ENV_VAR') or 'DEFAULT'
    LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'DEBUG'
    RESULT_FOLDER = os.environ.get('RESULT_FOLDER') or 'results/'
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # This is your Project Root

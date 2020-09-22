import logging

from flask import jsonify, send_from_directory, request
from flask_restplus import Resource

from infracheck import api
from infracheck.AuthenticationService import setup_basic_auth
from infracheck.Persistence import Persistence
from infracheck.PluginManager import PluginManager

log = logging.getLogger()
setup_basic_auth()
plugin_manager = PluginManager()
operations = api.namespace(
    'Test',
    path='/',
    description='test operation of the checkinfra backend')

plugin = api.namespace(
    'Plugins',
    path='/',
    description='api to get information on plugins')

authentication = api.namespace(
    'Authentication',
    path='/',
    description='all authentication operations of the checkinfra backend')

results = api.namespace(
    'Result',
    path='/',
    description='actions on results and logs')


@results.route('/results/<path:path>')
class Results(Resource):
    def get(self, path):
        return send_from_directory('../results/', path)


@plugin.route('/plugins')
class Plugins(Resource):
    def get(self):
        return jsonify(plugin_manager.list_plugins())


@results.route('/results')
class History(Resource):
    def get(self):
        limit = request.args.get('limit')
        offset = request.args.get('offset')
        res = Persistence().Result.query.all()[offset:limit]
        return jsonify(res)


@operations.route('/test')
class TestRunner(Resource):
    def post(self):
        data = request.get_json()
        res = plugin_manager.launch_tests(data)
        return jsonify(res)

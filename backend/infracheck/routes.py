import logging

from flask import jsonify, send_from_directory, request
from flask_restplus import Resource

from infracheck import Persistence
from infracheck import api
from infracheck.AuthenticationService import setup_basic_auth
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

presets = api.namespace(
    'Preset',
    path='/',
    description='actions on presets. currently not implemented')


@results.route('/results/<path:path>')
class Results(Resource):
    def get(self, path):
        return send_from_directory('../results/', path)


@plugin.route('/plugins')
class Plugins(Resource):
    def get(self):
        return jsonify(plugin_manager.list_plugins())


@results.route('/history')
class History(Resource):
    def get(self):
        limit = request.args.get('limit')
        offset = request.args.get('offset')
        if limit and offset:
            result = jsonify(Persistence().get_log(int(limit), int(offset)))
        else:
            result = jsonify(Persistence().get_log())
        return result


@operations.route('/test')
class TestRunner(Resource):
    def post(self):
        data = request.get_json()
        res = plugin_manager.launch_tests(data)
        return jsonify(res)


@presets.route('/preset')
class Preset(Resource):
    def get(self):
        limit = 10
        offset = 0
        return jsonify(Persistence().get_presets(int(limit), int(offset)))

    def post(self):
        data = request.get_json()
        res = Persistence().insert_preset(data)
        return jsonify(res)

import json
import logging
from typing import List

from flask import jsonify, send_from_directory, request
from flask_restplus import Resource
from jsonschema import validate

from infracheck import api
from infracheck.PluginManager import PluginManager
from infracheck.helper.schemes import test_data_scheme
from infracheck.model.TestInput import TestInput, PluginInput, ModuleInput
from infracheck.services.Persistence import Persistence

log = logging.getLogger()
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
        return jsonify(Persistence().Result.query.filter_by(id=path).first())


@results.route('/results/pdf/<path:path>')
class Results(Resource):
    def get(self, path):
        return send_from_directory('../results/', path)


@plugin.route('/plugins')
class Plugins(Resource):
    def get(self):
        return jsonify(plugin_manager.json)


@results.route('/results')
class Results(Resource):
    def get(self):
        limit = request.args.get('limit')
        offset = request.args.get('offset')
        res = Persistence().Result.query.all()[offset:limit]
        return jsonify(res)


@operations.route('/test')
class TestRunner(Resource):
    def post(self):
        json = request.get_json()
        validate(json, schema=test_data_scheme)
        data = convert_test_input_json_to_dataclasses(json)
        res = plugin_manager.launch_tests(data)
        return jsonify(res)


def convert_test_input_json_to_dataclasses(data: json):
    """
    Converts the test input from a dictionary to a data class
    This makes it easier to use and read it afterwards
    e.g.: data['plugins']['modules'] -> data.plugins.modules

    :param data:
    :return:
    """
    data = TestInput(**data)
    plugins: List[PluginInput] = list(PluginInput(**plugin_data) for plugin_data in data.plugins)
    for plugin in plugins:
        modules: List[ModuleInput] = list(ModuleInput(**module_data) for module_data in plugin.modules)
        plugin.modules = modules
    data.plugins = plugins
    return data

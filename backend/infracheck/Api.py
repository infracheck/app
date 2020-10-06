import json
import logging
from functools import wraps
from typing import List

import jsonschema
from flask import jsonify, send_from_directory, request
from flask_jwt_extended import create_access_token, verify_jwt_in_request, get_raw_jwt
from flask_restplus import Resource
from jsonschema import validate

from infracheck import api, app, jwt
from infracheck.PluginManager import PluginManager
from infracheck.helper.schemes import test_data_scheme
from infracheck.model.TestInput import TestInput, PluginInput, ModuleInput
from infracheck.services.Persistence import Persistence

log = logging.getLogger()
plugin_manager = PluginManager()
blacklist = set()


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist


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


def auth_required(fn):
    """ Decorator that checks if the correct JWT key is provided and though, the user is authenticated
    Can be configured with the 'SECURE_API' boolean variable

    :param fn:
    :return:
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        if app.config["SECURE_API"]:
            verify_jwt_in_request()
        return fn(*args, **kwargs)

    return wrapper


@results.route('/results/<path:path>')
class Results(Resource):
    @auth_required
    def get(self, path):
        return jsonify(Persistence().Result.query.filter_by(id=path).first())


@results.route('/results/pdf/<path:path>')
class Results(Resource):
    @auth_required
    def get(self, path):
        return send_from_directory('../results/', path)


@plugin.route('/plugins/flat')
class FlattenPlugins(Resource):
    @auth_required
    def get(self):
        """
        Returns available plugins in a smaller list
        containing only PluginIds and their ModuleIds
        :return:
        """
        return {
            plugin_id: {
                "modules": [
                    module_id
                    for module_id, module_data in plugin_data["modules"].items()],
                "author": plugin_data['author'],
                "version": plugin_data['version'],
                "compatibility": plugin_data['compatibility']
            }
            for plugin_id, plugin_data in plugin_manager.json.items()
        }


@plugin.route('/plugins')
class Plugins(Resource):
    @auth_required
    def get(self):
        """
        Returns all available plugins.
        :return:
        """
        return jsonify(plugin_manager.json)


@plugin.route('/plugins/<plugin_id>')
class SinglePlugin(Resource):
    @auth_required
    def get(self, plugin_id):
        """
        Returns the documentation and props of a single plugin
        :param plugin_id:
        :return:
        """
        return plugin_manager.json[plugin_id]


@plugin.route('/plugins/<plugin_id>/<module_id>')
class SingleModule(Resource):
    @auth_required
    def get(self, plugin_id, module_id):
        """
        Returns the documentation and props of a single module
        :param plugin_id:
        :param module_id:
        :return:
        """
        return plugin_manager.json[plugin_id]['modules'][module_id]


@results.route('/results')
class Results(Resource):
    @auth_required
    def get(self):
        limit = request.args.get('limit')
        offset = request.args.get('offset')
        res = Persistence().Result.query.all()[offset:limit]
        return jsonify(res)


@operations.route('/test')
class TestRunner(Resource):
    @auth_required
    def post(self):
        try:
            json = request.get_json()
            validate(json, schema=test_data_scheme)
            data = convert_test_input_json_to_dataclasses(json)
            res = plugin_manager.launch_tests(data)
            return jsonify(res)
        except jsonschema.exceptions.ValidationError as err:
            return repr(err), 400
        except ConnectionError as err:
            return repr(err), 408
        except PermissionError as err:
            return repr(err), 401


@authentication.route('/login')
class Login(Resource):
    def post(self):
        data = request.get_json()
        password = data['password']
        if not password:
            return {"msg": "Missing password parameter"}, 400

        if app.config["AUTH_PASSWORD"] != password:
            return {"msg": "Wrong password"}, 401

        access_token = create_access_token(identity='user')
        return {"access_token": access_token}, 200


@authentication.route('/logout')
class Logout(Resource):
    @auth_required
    def post(self):
        jti = get_raw_jwt()['jti']
        blacklist.add(jti)
        return {"msg": "Successfully logged out"}, 200


def convert_test_input_json_to_dataclasses(data: json):
    """
    Converts the test input from a dictionary to a data class
    This makes it easier to use and read it afterwards
    e.g.: data['plugins']['modules'] -> data.plugins.modules

    :param data:
    :return:
    """
    data = TestInput(**data)
    # PluginInput(**pluin_data)) generates a dataclass from a dict
    plugins: List[PluginInput] = list(PluginInput(**plugin_data) for plugin_data in data.plugins)
    for plugin in plugins:
        modules: List[ModuleInput] = list(ModuleInput(**module_data) for module_data in plugin.modules)
        plugin.modules = modules
    data.plugins = plugins
    return data

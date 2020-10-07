import json
import logging
from functools import wraps
from typing import List

import flask_jwt_extended
import jsonschema
from flask import jsonify, send_from_directory, request
from flask_jwt_extended import create_access_token, verify_jwt_in_request, get_raw_jwt, create_refresh_token, \
    jwt_refresh_token_required, get_jwt_identity
from flask_restplus import Resource, fields
from jsonschema import validate

from infracheck import api, app, jwt
from infracheck.PluginManager import PluginManager
from infracheck.helper.schemes import test_data_scheme, result_scheme, results_scheme, jwt_scheme, jwt_refresh_scheme, \
    plugins_output_scheme, plugin_output_scheme
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
    description='test operation of the CheckInfra backend')

plugin = api.namespace(
    'Plugins',
    path='/',
    description='api to get information on plugins')

authentication = api.namespace(
    'Authentication',
    path='/',
    description='all authentication operations of the CheckInfra backend')

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
            try:
                verify_jwt_in_request()
            except flask_jwt_extended.exceptions.NoAuthorizationError:
                return {"msg": "Missing Authorization Header"}, 401
        return fn(*args, **kwargs)

    return wrapper


@results.route('/results/<path:result_id>')
@results.response(200, 'Success', api.schema_model('TestResult', result_scheme))
class SingleResult(Resource):
    @auth_required
    def get(self, result_id):
        """
        Returns the test results of a single test, by it's id
        """
        return jsonify(Persistence().Result.query.filter_by(id=result_id).first())


@results.route('/results')
@results.response(200, 'Success', api.schema_model('TestResults', results_scheme))
class Results(Resource):
    @auth_required
    def get(self):
        """
        Returns a list of all test results.
        """
        limit = request.args.get('limit')
        offset = request.args.get('offset')
        res = Persistence().Result.query.all()[offset:limit]
        return jsonify(res)


@results.route('/results/pdf/<path:result_id>')
class PdfResult(Resource):
    @auth_required
    def get(self, result_id):
        """
        Returns the pdf document of a single test result, by it's id
        """
        return send_from_directory('../results/', result_id)


@plugin.route('/plugins/flat')
class FlattenPlugins(Resource):
    @auth_required
    def get(self):
        """
        Returns available plugins in a smaller list
        containing only PluginIds and their ModuleIds
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
    @plugin.response(200, 'Success', api.schema_model('Plugins Scheme', plugins_output_scheme))
    @auth_required
    def get(self):
        """
        Returns all available plugins.
        """
        return jsonify(plugin_manager.json)


@plugin.route('/plugins/<plugin_id>')
class SinglePlugin(Resource):
    @plugin.response(200, 'Success', api.schema_model('Plugin Scheme', plugin_output_scheme))
    @auth_required
    def get(self, plugin_id):
        """
        Returns the documentation and props of a single plugin
        """
        return plugin_manager.json[plugin_id]


@plugin.route('/plugins/<plugin_id>/<module_id>')
class SingleModule(Resource):
    @auth_required
    def get(self, plugin_id, module_id):
        """
        Returns the documentation and props of a single module
        """
        return plugin_manager.json[plugin_id]['modules'][module_id]


@operations.route(
    '/test',
    doc={
        "description": """
        This is the route that should be used for infrastructure testing.
        Before running tests, you should check which plugins you can use.
        For an easy start the use of the frontend is recommended.
        It supports you, creating your test cases and let you export your test data as JSON.
        That JSON can be used for this route.
        """
    })
@operations.doc(body=api.schema_model('TestData', test_data_scheme))
class TestRunner(Resource):
    @operations.response(200, 'Success', api.schema_model('TestResult', result_scheme))
    @operations.response(400, 'Connection error, when connecting to remote hosts')
    @operations.response(401, 'Permission error, when authenticating with remote hosts')
    @auth_required
    def post(self):
        """
        This route can be used to trigger a infrastructure check with InfraCheck.
        """
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


login_fields = api.model('Login Format', {
    'password': fields.String(description='Password to authenticate with the API', required=True),
})


@authentication.route('/login')
@authentication.doc(body=login_fields)
class Login(Resource):
    @authentication.response(200, 'Success', api.schema_model('JWT Login Format', jwt_scheme))
    @authentication.response(400, 'Missing password parameter')
    @authentication.response(401, 'Wrong password')
    def post(self):
        """
        Login with password only. Receive a JWT token as response, that can be used for further requests.
        """
        data = request.get_json()
        password = data['password']
        if not password:
            return {"msg": "Missing password parameter"}, 400

        if app.config["PASSWORD"] != password:
            return {"msg": "Wrong password"}, 401

        access_token = create_access_token(identity='user')
        refresh_token = create_refresh_token(identity='user')
        return {"access_token": access_token,
                "refresh_token": refresh_token,
                }, 200


@authentication.route('/refresh')
class Refresh(Resource):
    @authentication.response(200, 'Success', api.schema_model('JWT Refresh Format', jwt_refresh_scheme))
    @jwt_refresh_token_required
    def post(self):
        """
        JWT token requires refreshing. That can be done with this route.
        """
        current_user = get_jwt_identity()
        ret = {
            'access_token': create_access_token(identity=current_user)
        }
        return jsonify(ret), 200


@authentication.route('/logout')
class Logout(Resource):
    @auth_required
    @authentication.response(200, 'Successfully logged out')
    def post(self):
        """
        Logout and blacklist your old JWT token.
        """
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

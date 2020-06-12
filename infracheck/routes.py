import hashlib
import json

import flask
import flask_login
from flask import jsonify
from flask import request

from infracheck import app, login_manager, Persistence
from infracheck.Authentication import users, User
from infracheck.PluginManager import PluginManager

plugin_manager = PluginManager()


@app.route('/plugins', methods=['GET'])
def list_plugins():
    return jsonify(plugin_manager.list_plugins())


@app.route('/history', methods=['GET'])
def list_history():
    return jsonify(Persistence().get_log())


@app.route('/history/<path:log_id>', methods=['GET'])
def list_single_history(log_id: str):
    return jsonify(Persistence().get_log(str(log_id)))


@app.route('/test', methods=['POST'])
def run_test():
    raise NotImplementedError
    data = request.get_json()
    res = plugin_manager.launch_tests(data)
    return jsonify(res)


@app.route('/reload', methods=['GET'])
def reload_plugins():
    before = plugin_manager.list_plugins()
    plugin_manager.reload_plugins()
    after = plugin_manager.list_plugins()

    return {
        "message": "Reload successful",
        "updated": not json.dumps(before, sort_keys=True) == json.dumps(after, sort_keys=True)
    }


@app.route('/login', methods=['POST'])
def login():
    credentials = request.get_json()
    name, password = credentials["user"], credentials["password"]

    if hashlib.sha3_512(password.encode('UTF-8')).hexdigest() == users[name]['password']:
        user = User()
        user.id = name
        flask_login.login_user(user)
        return flask.redirect(flask.url_for('protected'))
    return 'Bad login'


@app.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'


@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'

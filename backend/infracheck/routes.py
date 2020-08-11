import hashlib

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
    limit = request.args.get('limit')
    offset = request.args.get('offset')
    if limit and offset:
        result = jsonify(Persistence().get_log(int(limit), int(offset)))
    else:
        result = jsonify(Persistence().get_log())
    return result


@app.route('/test', methods=['POST'])
def run_test():
    data = request.get_json()
    res = plugin_manager.launch_tests(data)
    return jsonify(res)


@app.route('/preset', methods=['POST', 'GET'])
def preset():
    if request.method == 'GET':
        limit = 10
        offset = 0
        return jsonify(Persistence().get_presets(int(limit), int(offset)))
    if request.method == 'POST':
        data = request.get_json()
        res = Persistence().insert_preset(data)
        return jsonify(res)


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

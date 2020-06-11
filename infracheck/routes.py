import json

from flask import jsonify
from flask import request

from infracheck import app
from infracheck.PluginManager import PluginManager

plugin_manager = PluginManager()


@app.route('/plugins', methods=['GET'])
def list_plugins():
    return jsonify(plugin_manager.list_plugins())


@app.route('/history', methods=['GET'])
def list_history():
    raise NotImplementedError


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

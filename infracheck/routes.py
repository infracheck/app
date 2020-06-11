from flask import jsonify
from flask import request

from infracheck import app
from infracheck.PluginManager import PluginManager

plugin_manager = PluginManager('plugins')


@app.route('/', methods=['POST'])
def add():
    data = request.get_json()
    plugin_manager.reload_plugins()
    res = plugin_manager.launch_tests(data)
    return jsonify(res)


@app.route('/plugins', methods=['GET'])
def list_plugins():
    return jsonify(plugin_manager.list_plugins())

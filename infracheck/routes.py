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


@app.route('/plugin/<path:name>/<path:version>', methods=['GET'])
def list_plugin(name, version):
    try:
        plugins = plugin_manager.list_plugins()
        return jsonify(list(filter(lambda x: x['version'] == version and x['name'] == name, plugins))[0])
    except IndexError as e:
        return str(F"Plugin with id {name}:{version} does not exist")

from flask import jsonify
from flask import request

from infracheck import app
from infracheck.PluginManager import PluginManager

plugins = PluginManager('plugins')


@app.route('/', methods=['POST'])
def add():
    data = request.get_json()
    plugins.reload_plugins()
    res = plugins.launch_tests(data)
    return jsonify(res)

import inspect
import json
import os
import subprocess
import uuid

from infracheck.model.IPlugin import PluginData, TestResult, IPlugin
from plugins.TestInfraPlugin.Config import Config


class TestInfraPlugin(IPlugin):
    package_name = F"{os.path.basename(__file__).split('.')[0]}"
    id = 'TestInfraPlugin'
    version = '0.1'
    documentation = """
    This Testinfra plugins enable you to run customized code snippets using the testinfra framework
    """

    def __init__(self):
        super().__init__()
        self.reload_modules()
        self.init()

    def init(self):
        """ Creates folders and everything for this test plugin
        :return:
        """
        if not os.path.exists(Config.OUTPUT_FOLDER):
            os.makedirs(Config.OUTPUT_FOLDER)

    def test(self, data: PluginData) -> TestResult:
        uid = uuid.uuid4().hex
        self.generate_test_file(data, uid)
        subprocess.call(F"py.test -v .out/{uid}.py", shell=True)
        data = {}
        return data

    def generate_test_file(self, test_data: json, uid: str):
        head = [
            'import pytest \n',
            '\n\n'
        ]
        body = []
        for test_module_data in test_data['set']:
            body.append(self.get_module_code(test_module_data))

        file_name = F".out/{uid}.py"
        file = open(file_name, 'w+')
        file.writelines(head + body)

    def get_module_code(self, data):
        uid = uuid.uuid4().hex
        module = list(filter(lambda x: x.id == data['id'] and x.version == data['version'], self.modules))[0]
        code_without_intend = ("\n" + inspect.getsource(module.test)).replace("\n    ", "\n")
        code_with_uuid = code_without_intend \
            .replace('def test(', F'def test_{uid}(') \
            .replace('fields', F'fields_{uid}')
        return F"fields_{uid} = {json.dumps(data['fields'])}\n" + code_with_uuid

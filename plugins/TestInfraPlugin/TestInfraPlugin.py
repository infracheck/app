import inspect
import json
import os
import subprocess
import uuid
from typing import List

from infracheck.helper.KeyRegistrationHelper import KeyRegistrationHelper
from infracheck.model.DataTypes import DataTypes
from infracheck.model.IPlugin import TestResult, IPlugin
from infracheck.model.ITestData import IPluginData, IModuleData, IGeneralPluginData
from infracheck.model.ITestModule import ITestModule
from plugins.TestInfraPlugin.Config import Config


class TestInfraPluginData(IGeneralPluginData):
    hosts: List[str]
    username: str
    password: str


class TestInfraPlugin(IPlugin):
    package_name = F"{os.path.basename(__file__).split('.')[0]}"
    name = 'TestInfraPlugin'
    documentation = """
    This Testinfra plugins enable you to run customized code snippets using the testinfra framework
    """
    data: TestInfraPluginData = {
        "hosts": DataTypes.TextList,
        "username": DataTypes.TextList,
        "target_os": DataTypes.Text,
        "password": DataTypes.TextList,
    }

    def __init__(self):
        super().__init__()
        self.ssh_key_helper = KeyRegistrationHelper(self.data['username'], self.data['password'])
        self.reload_modules()
        self.init()

    def init(self):
        """ Creates folders and everything for this test plugin
        :return:
        """
        if not os.path.exists(Config.OUTPUT_FOLDER):
            os.makedirs(Config.OUTPUT_FOLDER)

    def test(self, data: IPluginData) -> TestResult:
        super().test(data)

        self.register_ssh_keys()

        uid = uuid.uuid4().hex
        self.generate_test_file(data, uid)
        subprocess.call(F"py.test -v .out/{uid}.py", shell=True)
        data = {}

        self.clean_ssh_keys()
        return data

    def generate_test_file(self, test_data: IPluginData, uid: str):
        """ Creates a testfile and replaces all placeholders with the actual test data """
        head = [
            'import pytest \n',
            '\n\n'
        ]
        body = []
        for test_module_data in test_data['modules']:
            body.append(self.get_module_code(test_module_data))

        file_name = F".out/{uid}.py"
        file = open(file_name, 'w+')
        file.writelines(head + body)
        file.close()

    def get_module_code(self, data: IModuleData):
        """ Extracts test() function from modules and replaces the placeholders it with real data

        :param data:
        :return:
        """
        uid = uuid.uuid4().hex
        module: ITestModule = \
            list(filter(lambda x: x.name == data['name'], self.modules))[0]
        code_without_intend = ("\n" + inspect.getsource(module.test)).replace("\n    ", "\n")
        code_with_uuid = code_without_intend \
            .replace('def test(', F'def test_{uid}(') \
            .replace('fields', F'fields_{uid}')
        return F"fields_{uid} = {json.dumps(data['fields'])}\n\n{code_with_uuid}\n\n"

    def register_ssh_keys(self):
        if self.data['target_os'] == 'linux':
            for host in self.data['hosts']:
                self.ssh_key_helper.register_ssh_key_on_host(host)

    def clean_ssh_keys(self):
        if self.data['target_os'] == 'linux':
            for host in self.data['hosts']:
                self.ssh_key_helper.remove_ssh_key(host)

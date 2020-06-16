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
        self.reload_modules()
        self.init()

    def init(self):
        """ Creates folders and everything for this test plugin
        :return:
        """
        if not os.path.exists(Config.OUTPUT_FOLDER):
            os.makedirs(Config.OUTPUT_FOLDER)

    def test(self, _data: IPluginData) -> TestResult:
        super().test(_data)
        ssh_service = KeyRegistrationHelper(self.data['username'], self.data['password'])
        if self.data["target_os"] == 'linux':
            ssh_service.register_ssh_keys(self.data['hosts'])

        uid = uuid.uuid4().hex
        self.generate_test_file(_data, uid)
        self.create_test_command_and_launch_test(uid)
        # subprocess.call(F"py.test -v .out/{uid}.py", shell=True)
        data = {}

        if self.data["target_os"] == 'linux':
            ssh_service.clean_ssh_keys(self.data['hosts'])
        return data

    def create_test_command_and_launch_test(self, uid):
        config_string = F"--junit-xml={Config.OUTPUT_FOLDER}/result_{uid}.xml"
        host_string = self.create_hosts_string()
        cmd: str = F"py.test {Config.OUTPUT_FOLDER}/test_{uid}.py {host_string} {config_string} "
        subprocess.call(cmd, shell=True)

    def create_hosts_string(self):
        if self.data['target_os'] == 'linux':
            hosts_with_auth = list(
                map(lambda host: F"ssh://{self.data['username']}@{host}", self.data['hosts']
                    )
            )
            host_string = ','.join(map(str, hosts_with_auth))
            os_specific_cmd_part = F"--ssh-identity-file='key/id_rsa' --hosts='{host_string}'"
        else:
            hosts_with_auth = list(
                map(lambda host:
                    F"winrm://{self.data['username']}:{self.data['password']}@{host}:5985?no_ssl=true&no_verify_ssl=true",
                    self.data['hosts']
                    )
            )
            host_string = ','.join(map(str, hosts_with_auth))
            os_specific_cmd_part = F"--hosts='{host_string}'"
        return os_specific_cmd_part

    def generate_test_file(self, test_data: IPluginData, uid: str):
        """ Creates a testfile and replaces all placeholders with the actual test data """
        head = [
            'import pytest \n',
            '\n\n'
        ]
        body = []
        for test_module_data in test_data['modules']:
            body.append(self.get_module_code(test_module_data))

        file_name = F".out/test_{uid}.py"
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

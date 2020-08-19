import inspect
import json
import os
import subprocess
import uuid
from typing import Dict

import xml.dom.minidom

from infracheck.model.DataTypes import DataTypes
from infracheck.model.IModule import IModule
from infracheck.model.IParam import IParam
from infracheck.model.IPlugin import IPlugin
from infracheck.model.ITestData import IPluginData, IModuleData
from infracheck.model.ITestResult import IPluginResult
from plugins.testinfra.Config import Config
from plugins.testinfra.KeyRegistrationHelper import KeyRegistrationHelper


class TestInfraPlugin(IPlugin):
    id = 'testinfra'
    version = 0.1
    documentation = """
    This Testinfra plugins enable you to run customized code snippets using the testinfra framework.
    
    **Note:** You can run tests on this machine too. For that, simply enter ['localhost'] to your hosts array. 
    In that case you dont need any username or password at all.
    """
    params: Dict[str, IParam] = {
        "hosts": {
            "type": DataTypes.TextList,
            "value": ['localhost']
        },
        "username": {
            "type": DataTypes.Text,
            "value": "username"
        },
        "target_os": {
            "type": DataTypes.Text,
            "value": "linux"
        },
        "password": {
            "type": DataTypes.Password,
            "value": "password"
        },
        "port": {
            "type": DataTypes.Number,
            "value": 22
        }
    }

    @staticmethod
    def init_env():
        """ Creates folders and everything for this test plugin
        :return:
        """
        if not os.path.exists(Config.OUTPUT_FOLDER):
            os.makedirs(Config.OUTPUT_FOLDER)

    def test(self, _data: IPluginData) -> IPluginResult:
        """
        The complete test run
        1. Setup environment
        2. Create test uid
        3. Register ssh keys on remote hosts
        4. Generate test files
        5. Launch tests
        6. Remove remote ssh keys
        7. Create results

        :param _data:
        :return:
        """
        super().test(_data)
        self.init_env()
        uid = uuid.uuid4().hex

        # Catch special case if tests should be performend on localhost only
        if self.params['hosts'] == ['localhost']:
            self.generate_test_file(_data, uid)
            self.create_test_command_and_launch_test(uid, localhost_only=True)
            return self.create_result_from_xml_output(uid)

        ssh_service = KeyRegistrationHelper(self.params['username'], self.params['password'])
        if self.params["target_os"] == 'linux':
            ssh_service.register_ssh_keys(self.params['hosts']['value'])

        self.generate_test_file(_data, uid)
        self.create_test_command_and_launch_test(uid)

        if self.params["target_os"] == 'linux':
            ssh_service.clean_ssh_keys(self.params['hosts']['value'])

        return self.create_result_from_xml_output(uid)

    def create_test_command_and_launch_test(self, uid, localhost_only: bool = False):
        config_string = F"--junit-xml={Config.OUTPUT_FOLDER}result_{uid}.xml "
        host_string = self.create_hosts_string()
        if localhost_only:
            cmd: str = F"py.test {Config.OUTPUT_FOLDER}test_{uid}.py {config_string} "
        else:
            cmd: str = F"py.test {Config.OUTPUT_FOLDER}test_{uid}.py {host_string} {config_string} "
        subprocess.call(cmd, shell=True)

    def create_hosts_string(self):
        if self.params['target_os'] == 'linux':
            hosts_with_auth = list(
                map(lambda host: F"ssh://{self.params['username']}@{host}", self.params['hosts'])
            )
            host_string = ','.join(map(str, hosts_with_auth))
            os_specific_cmd_part = F"--ssh-identity-file='{Config.SSH_FOLDER}id_rsa' --hosts='{host_string}'"
        else:
            hosts_with_auth = list(
                map(lambda host:
                    F"winrm://{self.params['username']}:{self.params['password']}@{host}:5985?no_ssl=true&no_verify_ssl=true",
                    self.params['hosts']
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
        test_id = 0
        for test_module_data in test_data['modules']:
            body.append(self.get_module_code(test_module_data, test_id))
            test_id += 1

        file_name = F"{Config.OUTPUT_FOLDER}test_{uid}.py"
        file = open(file_name, 'w+')
        file.writelines(head + body)
        file.close()

    def get_module_code(self, data: IModuleData, test_id: int):
        """ Extracts test() function from modules and replaces the placeholders with real data

        :param test_id:
        :param data:
        :return:
        """
        module: IModule = \
            list(filter(lambda x: x.id == data['id'], self.modules))[0]
        code_without_intend = ("\n" + inspect.getsource(module.test)).replace("\n    ", "\n")
        code_with_uuid = code_without_intend \
            .replace('def test(', F'def test_{module.id}_{test_id}(') \
            .replace('fields', F'fields_{test_id}')
        return F"fields_{test_id} = {json.dumps(data['fields'])}\n\n{code_with_uuid}\n\n"

    def create_result_from_xml_output(self, uid):
        xml_file = Config.OUTPUT_FOLDER + '/result_' + uid + '.xml'
        input_file = xml.dom.minidom.parse(xml_file)
        data = input_file.getElementsByTagName("testsuite")[0]

        result: IPluginResult = {
            "plugin_name": self.id,
            "plugin_version": self.version,
            "succeeded": int(data.getAttribute("tests")) - int(data.getAttribute("failures")),
            "failures": int(data.getAttribute("failures")),
            "errors": int(data.getAttribute("errors")),
            "total": int(data.getAttribute("tests")),
            "message": "",
            "custom_data": []
        }
        test_cases = input_file.getElementsByTagName("testcase")
        for test in test_cases:
            test_data = {
                "name": test.getAttribute("name"),
                "host": test.getAttribute("name").split('[')[1].split(']')[0].rsplit('-', 1)[0],
                "time": test.getAttribute("time")
            }
            if test.getElementsByTagName("failure"):
                success = False
                test_data["message"] = test.getElementsByTagName("failure")[0].getAttribute("message")
            else:
                success = True

            test_data["success"] = success
            result["custom_data"].append(test_data)
        return result

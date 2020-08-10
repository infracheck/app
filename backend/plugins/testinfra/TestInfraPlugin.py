import datetime
import inspect
import json
import os
import subprocess
import uuid
import xml.dom.minidom
from typing import List

from infracheck.model.DataTypes import DataTypes
from infracheck.model.IPlugin import IPlugin
from infracheck.model.ITestData import IPluginData, IModuleData, IGeneralPluginData
from infracheck.model.ITestModule import ITestModule
from infracheck.model.ITestResult import TestResult
from plugins.testinfra.Config import Config
from plugins.testinfra.KeyRegistrationHelper import KeyRegistrationHelper


class TestInfraPluginData(IGeneralPluginData):
    hosts: List[str]
    username: str
    password: str


class TestInfraPlugin(IPlugin):
    id = 'testinfra'
    version = 0.1
    documentation = """
    This Testinfra plugins enable you to run customized code snippets using the testinfra framework
    """
    data: TestInfraPluginData = {
        "hosts": DataTypes.TextList,
        "username": DataTypes.Text,
        "target_os": DataTypes.Text,
        "password": DataTypes.Text,
        "port": DataTypes.Number
    }

    @staticmethod
    def init_env():
        """ Creates folders and everything for this test plugin
        :return:
        """
        if not os.path.exists(Config.OUTPUT_FOLDER):
            os.makedirs(Config.OUTPUT_FOLDER)

        # Create ssh key
        if not os.path.exists(Config.SSH_FOLDER):
            os.makedirs(Config.SSH_FOLDER)
        subprocess.run(F"echo -e 'y\n' | ssh-keygen -q -t rsa -N '' -f {Config.SSH_FOLDER}id_rsa", shell=True,
                       check=True)

    def test(self, _data: IPluginData) -> TestResult:
        super().test(_data)
        self.init_env()
        uid = uuid.uuid4().hex

        ssh_service = KeyRegistrationHelper(self.data['username'], self.data['password'])
        if self.data["target_os"] == 'linux':
            ssh_service.register_ssh_keys(self.data['hosts'])

        self.generate_test_file(_data, uid)
        self.create_test_command_and_launch_test(uid)

        if self.data["target_os"] == 'linux':
            ssh_service.clean_ssh_keys(self.data['hosts'])

        return self.convert_result_to_csv(uid)

    def create_test_command_and_launch_test(self, uid):
        config_string = F"--junit-xml={Config.OUTPUT_FOLDER}result_{uid}.xml "
        host_string = self.create_hosts_string()
        cmd: str = F"py.test {Config.OUTPUT_FOLDER}test_{uid}.py {host_string} {config_string} "
        subprocess.call(cmd, shell=True)

    def create_hosts_string(self):
        if self.data['target_os'] == 'linux':
            hosts_with_auth = list(
                map(lambda host: F"ssh://{self.data['username']}@{host}", self.data['hosts']
                    )
            )
            host_string = ','.join(map(str, hosts_with_auth))
            os_specific_cmd_part = F"--ssh-identity-file='{Config.SSH_FOLDER}id_rsa' --hosts='{host_string}'"
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
        module: ITestModule = \
            list(filter(lambda x: x.id == data['id'], self.modules))[0]
        code_without_intend = ("\n" + inspect.getsource(module.test)).replace("\n    ", "\n")
        code_with_uuid = code_without_intend \
            .replace('def test(', F'def test_{module.id}_{test_id}(') \
            .replace('fields', F'fields_{test_id}')
        return F"fields_{test_id} = {json.dumps(data['fields'])}\n\n{code_with_uuid}\n\n"

    @staticmethod
    def convert_result_to_csv(uid):
        xml_file = Config.OUTPUT_FOLDER + '/result_' + uid + '.xml'
        input_file = xml.dom.minidom.parse(xml_file)
        result = {
            "id": uid,
            "date": datetime.datetime.today().strftime('%m/%d/%Y-%H:%M'),
        }

        testsuite_keys = [
            "errors",
            "failures",
            "skipped",
            "tests"
        ]

        testsuite = input_file.getElementsByTagName("testsuite")[0]
        for key in testsuite_keys:
            result[key] = int(testsuite.getAttribute(key))

        result['total'] = result['tests']
        result['succeeded'] = result['total'] - result['failures']

        result["testset"] = []
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
            result["testset"].append(test_data)
        return result

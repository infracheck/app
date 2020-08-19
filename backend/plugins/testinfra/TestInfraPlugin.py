import logging
import unittest
from typing import Dict, List

import testinfra

from infracheck.model.DataTypes import DataTypes
from infracheck.model.IModule import IModule
from infracheck.model.IParam import IParam
from infracheck.model.IPlugin import IPlugin
from infracheck.model.ITestData import IPluginData
from infracheck.model.ITestResult import IPluginResult, IModuleResult
from plugins.testinfra.Config import Config
from plugins.testinfra.KeyRegistrationHelper import KeyRegistrationHelper

log = logging.getLogger()


class TestInfraPlugin(IPlugin):
    id = 'testinfra'
    version = 0.1
    documentation = """
    This Testinfra plugins enable you to run customized code snippets using the testinfra framework.
    
    **Note:** You can run tests on this machine too. For that, simply enter ['localhost'] to your hosts array. 
    In that case you dont need any username or password at all.
    """
    params: Dict[str, IParam] = {
        "host": {
            "type": DataTypes.Text,
            "value": 'localhost'
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

    def test(self, plugin_data: IPluginData) -> IPluginResult:
        """
        :param plugin_data:
        :return:
        """
        host_address = plugin_data['params']['hosts']['value']
        username = plugin_data['params']['username']['value']
        target_os = plugin_data['params']['target_os']['value']
        password = plugin_data['params']['password']['value']
        port = plugin_data['params']['port']['value']

        if host_address == 'localhost':
            host = testinfra.get_host("local://")
        else:
            ssh_service = KeyRegistrationHelper(self.params['username'], self.params['password'])
            if self.params["target_os"] == 'linux':
                ssh_service.register_ssh_keys([self.params['hosts']['value']])
            host = testinfra.get_host(F"paramiko://{username}@{host_address}", ssh_config=F"{Config.SSH_FOLDER}id_rsa")

        runner = unittest.TextTestRunner()
        suite = unittest.TestSuite()
        for module in plugin_data['modules']:
            test: [IModule, unittest.TestCase] = self.get_module_by_id(module['id'])('test')
            test.host = host
            # Set parameters and replace default values
            for param in test.params.keys():
                try:
                    test.params[param]['value'] = module['params'][param]
                except KeyError as e:
                    log.info(F"Parameter {e} not set -> using default value: '{test.params[param]['value']}'")
            suite.addTest(test)

        result: unittest.TestResult = runner.run(suite)

        module_data: List[IModuleResult] = [
            {
                "module_name": "str",
                "module_version": 0.1,
                "fields": "Any",
                "success": True,
                "message": "str"
            }
        ]
        res: IPluginResult = {
            "plugin_name": self.id,
            "plugin_version": self.version,
            "succeeded": result.wasSuccessful(),
            "failures": len(result.failures),
            "errors": len(result.errors),
            "total": result.testsRun,
            "message": str(result.failures),
            "module_data": module_data,
            "custom_data": {}
        }
        if self.params["target_os"] == 'linux':
            ssh_service.clean_ssh_keys([self.params['hosts']['value']])
        return res

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
from plugins.testinfra.KeyRegistrationHelper import KeyRegistrationHelper
from plugins.testinfra.TestInfraConnector import ParamikoConnector, WinRmConnector

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
        # 1. Extract parameters
        host_address = plugin_data['params']['host']
        username = plugin_data['params']['username']
        target_os = plugin_data['params']['target_os']
        password = plugin_data['params']['password']
        port = plugin_data['params']['port']

        # 2. Get host
        if host_address == 'localhost':
            host = testinfra.get_host("local://")
        elif target_os == 'linux':
            ssh_service = KeyRegistrationHelper(
                user=username,
                password=password,
                port=port
            )
            ssh_service.register_ssh_keys([host_address])
            host = ParamikoConnector(
                username=username,
                password=password,
                host=host_address,
                port=port
            ).get_host()
        elif target_os == 'windows':
            host = WinRmConnector(
                username=username,
                password=password,
                host=host_address,
                port=port
            ).get_host()

        # 3. Run Test
        runner = unittest.TextTestRunner()
        results: List[unittest.TestResult] = []
        module_results: List[IModuleResult] = []
        for module in plugin_data['modules']:
            test: [IModule, unittest.TestCase] = self.get_module_by_id(module['id'])('test')
            test.host = host
            # Set parameters and replace default values
            for param in test.params.keys():
                try:
                    test.params[param]['value'] = module['params'][param]
                except KeyError as e:
                    log.info(F"Parameter {e} not set -> using default value: '{test.params[param]['value']}'")

            test_result = runner.run(test)
            results.append(test_result)
            module_results.append({
                "module_name": module['id'],
                "module_version": test.version,
                "params": module['params'],
                "is_successful": test_result.wasSuccessful(),
                "message": str(test_result.failures)
            })

        # 4. Create Result
        res: IPluginResult = {
            "plugin_name": self.id,
            "plugin_version": self.version,
            "success_count": sum(c.testsRun for c in results) - sum(not c['is_successful'] for c in module_results),
            "failure_count": sum(len(c.failures) for c in results),
            "error_count": sum(len(c.errors) for c in results),
            "total_count": sum(c.testsRun for c in results),
            "message": "hello world",
            "module_result": module_results,
            "custom_data": {}
        }
        if self.params["target_os"] == 'linux':
            ssh_service.clean_ssh_keys([self.params['hosts']['value']])
            del ssh_service
        return res

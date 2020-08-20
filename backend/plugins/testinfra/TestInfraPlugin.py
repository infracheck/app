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

        # 2. Generate host-string
        if host_address == 'localhost':
            host = testinfra.get_host("local://")
        else:
            ssh_service = KeyRegistrationHelper(self.params['username'], self.params['password'])
            if self.params["target_os"] == 'linux':
                # Perform 'ssh-copy-id' to register ssh keys on remote machine
                ssh_service.register_ssh_keys([self.params['hosts']['value']])
            host = testinfra.get_host(F"paramiko://{username}@{host_address}", ssh_config=F"{Config.SSH_FOLDER}id_rsa")

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

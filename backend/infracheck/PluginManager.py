import logging
import uuid
from typing import List

from jsonschema import validate

from infracheck.helper.load_packages import load_packages
from infracheck.helper.schemes import test_data_scheme
from infracheck.model.IPlugin import IPlugin
from infracheck.model.ITestData import ITestData
from infracheck.model.ITestResult import ITestResult

from infracheck.Persistence import Persistence

log = logging.getLogger()


class PluginManager(object):
    """Upon creation, this class will read the plugins package for modules
    that contain a class definition that is inheriting from the Plugin class
    """

    plugins: List[IPlugin] = []
    database = Persistence()

    def list_plugins(self):
        """Returns a list of plugins that are available
        """
        res = list({
                       "id": x.id,
                       "documentation": x.documentation,
                       "modules": x.list_modules(),
                       "data": x.data,
                       "type": "plugin"
                   } for x in self.plugins)
        return res

    def __init__(self):
        """Constructor that initiates the reading of all available plugins
        when an instance of the PluginCollection object is created
        """
        self._reload_plugins()

    def _reload_plugins(self):
        """Reset the list of all plugins and initiate the walk over the main
        provided plugin package to load all available plugins
        """
        self.plugins: List[IPlugin] = load_packages('plugins', IPlugin)

    def launch_tests(self, data: ITestData) -> ITestResult:
        """ Run all tests defined in the json

        :param data:
        :return:
        """
        uid = uuid.uuid4().hex
        is_not_valid = validate(instance=data, schema=test_data_scheme)
        if is_not_valid:
            raise TypeError(is_not_valid)

        result: ITestResult = {
            ""
            "data": []
        }
        log.info(F"Launching the test with name: {data['name']}")
        for plugin_test_data in data['plugins']:
            result['data'].append(
                self._get_test_plugin(plugin_test_data['id']).test(
                    plugin_test_data))

        result['id'] = uid
        result = self.serialize_result(data, result)
        self.database.insert_test_result(result)
        return result

    def _get_test_plugin(self, plugin_name: str) -> IPlugin:
        """ Returns the right plugin object, receiving id and version

        :param plugin_name:
        :return:
        """
        return list(filter(lambda plugin: plugin.id == plugin_name, self.plugins))[0]

    @staticmethod
    def serialize_result(input_data: ITestData, result_data: ITestResult) -> ITestResult:
        """ Takes multiple plugin results and serialize them to one response
        """
        result = {
            "id": result_data['id'],
            "name": input_data['name'],
            "description": input_data['description'],
            "succeeded": sum(c['succeeded'] for c in result_data['data']),
            "failures": sum(c['failures'] for c in result_data['data']),
            "errors": sum(c['errors'] for c in result_data['data']),
            "total": sum(c['total'] for c in result_data['data']),
            "message": "PLEASE IMPLEMENT",
            "date": "",
            "data": result_data
        }
        if result["failures"] == 0:
            result["message"] = 'Test complete. No failures.'
        else:
            result["message"] = F"Test complete but {result['failures']} failure detected."

        return result

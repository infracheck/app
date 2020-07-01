import logging
from typing import List

from infracheck.helper.load_packages import load_packages
from infracheck.model.IPlugin import IPlugin
from infracheck.model.ITestData import ITestData

log = logging.getLogger()


class ITestResult(object):
    # TODO Implement
    pass


class PluginManager(object):
    """Upon creation, this class will read the plugins package for modules
    that contain a class definition that is inheriting from the Plugin class
    """

    plugins: List[IPlugin] = []

    def list_plugins(self):
        """Returns a list of plugins that are available
        """
        res = list({
                       "id": x.id,
                       "documentation": x.documentation,
                       "modules": x.list_modules(),
                       "data": x.expected_data,
                       "type": "plugin",

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
        result = []
        log.info(F"Launching the test with name: {data['id']}")
        for plugin_test_data in data['plugins']:
            result.append(
                self._get_test_plugin(plugin_test_data['id']).test(
                    plugin_test_data))
        return result

    def _get_test_plugin(self, plugin_name: str) -> IPlugin:
        """ Returns the right plugin object, receiving id and version

        :param plugin_name:
        :return:
        """
        return list(filter(lambda plugin: plugin.id == plugin_name, self.plugins))[0]

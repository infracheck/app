import inspect
import logging
from typing import List

from infracheck.helper.load_packages import load_packages
from infracheck.model.IPlugin import IPlugin
from infracheck.model.ITestData import ITestData

log = logging.getLogger()


class PluginManager(object):
    """Upon creation, this class will read the plugins package for modules
    that contain a class definition that is inheriting from the Plugin class
    """

    plugins: List[IPlugin] = []

    def list_plugins(self):
        """Returns a list of plugins that are available
        """
        res = list({
                       "name": x.name,
                       "version": x.version,
                       "package_id": x.package_name,
                       "documentation": x.documentation,
                       "modules": x.list_modules(),
                       "used_packages": x.requirements,
                       "data": x.data,

                   } for x in self.plugins)
        return res

    def __init__(self):
        """Constructor that initiates the reading of all available plugins
        when an instance of the PluginCollection object is created
        """
        self.reload_plugins()

    def reload_plugins(self):
        """Reset the list of all plugins and initiate the walk over the main
        provided plugin package to load all available plugins
        """
        self.plugins: List[IPlugin] = load_packages('plugins', IPlugin)

    def launch_tests(self, data: ITestData):
        """ Run all tests defined in the json

        :param data:
        :return:
        """
        result = []
        log.info(F"Launching the test with name: {data['name']}")
        for plugin_test_data in data['plugins']:
            result.append(
                self.get_test_plugin(plugin_test_data['name'], plugin_test_data['version']).test(
                    plugin_test_data))
        return result

    def get_test_plugin(self, plugin_name: str, version: str) -> IPlugin:
        """ Returns the right plugin object, receiving id and version

        :param plugin_name:
        :param version:
        :return:
        """
        return list(filter(lambda plugin: plugin.name == plugin_name and plugin.version == version, self.plugins))[0]

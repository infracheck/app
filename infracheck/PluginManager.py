from typing import List

from infracheck.helper.load_packages import load_packages
from infracheck.model.IPlugin import IPlugin


class PluginManager(object):
    """Upon creation, this class will read the plugins package for modules
    that contain a class definition that is inheriting from the Plugin class
    """

    plugins: List[IPlugin] = []

    def list_plugins(self):
        """Returns a list of plugins that are available
        """
        res = list({
                       "name": x.id,
                       "version": x.version,
                       "package_id": x.package_name,
                       "documentation": x.documentation,
                       "module_count": len(x.modules),
                       "modules": x.list_modules(),
                       "used_packages": x.requirements,
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

    def launch_tests(self, data):
        """ Run all tests defined in the json

        :param data:
        :return:
        """
        result = []
        for plugin_test_data in data['tests']:
            result.append(
                self.get_test_plugin(plugin_test_data['id'], plugin_test_data['version']).test(plugin_test_data['data']))
        return result

    def get_test_plugin(self, plugin_id: str, version: str) -> IPlugin:
        """ Returns the right plugin object, receiving id and version

        :param plugin_id:
        :param version:
        :return:
        """
        return list(filter(lambda plugin: plugin.id == plugin_id and plugin.version == version, self.plugins))[0]

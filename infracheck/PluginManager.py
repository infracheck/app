import inspect
import os
import pkgutil
from typing import List

from infracheck.Plugin import IPlugin


class PluginManager(object):
    """Upon creation, this class will read the plugins package for modules
    that contain a class definition that is inheriting from the Plugin class
    """

    def list_plugins(self):
        """Returns a list of plugins that are available
        """
        res = list(map(lambda x:
                       {
                           "name": x.id,
                           "version": x.version,
                           "documentation": x.documentation,
                       }
                       , self.plugins))
        print(res)
        return res

    def __init__(self, plugin_package):
        """Constructor that initiates the reading of all available plugins
        when an instance of the PluginCollection object is created
        """
        self.plugin_package = plugin_package
        self.reload_plugins()

    def reload_plugins(self):
        """Reset the list of all plugins and initiate the walk over the main
        provided plugin package to load all available plugins
        """
        self.plugins: List[IPlugin] = []
        self.seen_paths = []
        print()
        print(f'Looking for plugins under package {self.plugin_package}')
        self.walk_package(self.plugin_package)

    def launch_tests(self, data):
        """ Run all tests defined in the json

        :param data:
        :return:
        """
        result = []
        for plugin in self.plugins:
            if str(plugin) in data:
                result.append(plugin.test(data[str(plugin)]['data']))
        return result

    def walk_package(self, package):
        """Recursively walk the supplied package to retrieve all plugins
        """
        imported_package = __import__(package, fromlist=['blah'])

        for _, pluginname, ispkg in pkgutil.iter_modules(imported_package.__path__, imported_package.__name__ + '.'):
            if not ispkg:
                plugin_module = __import__(pluginname, fromlist=['blah'])
                clsmembers = inspect.getmembers(plugin_module, inspect.isclass)
                for (_, c) in clsmembers:
                    # Only add classes that are a sub class of Plugin, but NOT Plugin itself
                    if issubclass(c, IPlugin) & (c is not IPlugin):
                        print(f'    Found plugin class: {c.__module__}.{c.__name__}')
                        self.plugins.append(c())

        # Now that we have looked at all the modules in the current package, start looking
        # recursively for additional modules in sub packages
        all_current_paths = []
        if isinstance(imported_package.__path__, str):
            all_current_paths.append(imported_package.__path__)
        else:
            all_current_paths.extend([x for x in imported_package.__path__])

        for pkg_path in all_current_paths:
            if pkg_path not in self.seen_paths:
                self.seen_paths.append(pkg_path)

                # Get all sub directory of the current package path directory
                child_pkgs = [p for p in os.listdir(pkg_path) if os.path.isdir(os.path.join(pkg_path, p))]

                # For each sub directory, apply the walk_package method recursively
                for child_pkg in child_pkgs:
                    self.walk_package(package + '.' + child_pkg)

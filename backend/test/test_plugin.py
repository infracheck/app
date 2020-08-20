import inspect
import unittest

from infracheck.PluginManager import PluginManager


class PluginsTest(unittest.TestCase):
    def setUp(self):
        self.plugin_manager = PluginManager()

    def test_plugins(self):
        with self.subTest("'testinfra' exists"):
            self.assertTrue(any(x.id == "testinfra" for x in self.plugin_manager.plugins))

        with self.subTest("'demo_plugin' exists"):
            self.assertTrue(any(x.id == "demo_plugin" for x in self.plugin_manager.plugins))

        for plugin in self.plugin_manager.plugins:
            with self.subTest(F"test() is implemented in {plugin.id}"):
                methods = inspect.getmembers(plugin, inspect.ismethod)
                self.assertTrue(any(x[0] == "test" for x in methods))

import unittest

from infracheck.Plugin import Plugin
from infracheck.PluginManager import PluginManager
from plugins.DemoPlugin.DemoPlugin import DemoPlugin


class PluginsTest(unittest.TestCase):
    def setUp(self):
        self.plugin_manager = PluginManager()

    def test_PluginInterface(self):
        with self.subTest(F"init throws TypeError because abstract methods are missing"):
            with self.assertRaises(TypeError):
                Plugin()

    def test_PluginManager(self):
        with self.subTest(F"has plugins"):
            self.assertTrue(len(self.plugin_manager._plugins) > 0)



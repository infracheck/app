import unittest

from infracheck.PluginManager import PluginManager
from infracheck.model.Plugin import Plugin
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

    def test_DemoPlugin(self):
        plugin = DemoPlugin()

        with self.subTest("'DemoPlugin' getter works"):
            self.assertIsInstance(plugin, Plugin)

        with self.subTest(F"has a id"):
            self.assertIsNotNone(plugin.__id__)

        with self.subTest(F"has a documentation"):
            self.assertIsNotNone(plugin.__documentation__)
            self.assertTrue(len(plugin.__documentation__) >= 0)

        with self.subTest(F"has a version hint"):
            self.assertIsNotNone(plugin.__version__)
            self.assertIsInstance(plugin.__version__, float)

        with self.subTest(F"has a properties definition"):
            self.assertIsNotNone(plugin.props)

        with self.subTest(F"has modules"):
            self.assertIsNotNone(plugin.json)

        with self.subTest(F"has more then one module"):
            self.assertTrue(len(plugin.json.items()) > 0)

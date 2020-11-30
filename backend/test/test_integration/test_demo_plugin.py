import unittest

from infracheck.PluginManager import PluginManager


class DemoPluginTest(unittest.TestCase):
    """
    E-5 - Demo-Plugin
    """

    def test_valid_demo_plugin_format(self):
        plugin_id = "DemoPlugin"
        module_id = "DemoModule"
        with self.subTest(F"'{plugin_id}' exists"):
            plugin = PluginManager()._get_plugin_instance(plugin_id)
            self.assertTrue(plugin.__id__ == plugin_id, F"'{plugin_id}' exists")

        with self.subTest(F"'{plugin_id}' has just one module"):
            self.assertEqual(len(plugin._modules), 1)

        with self.subTest(F"'{plugin_id}' has a '{module_id}' module"):
            module = plugin._get_module_instance(module_id)
            self.assertTrue(module.__id__ == module_id, F"'{module_id}' exists")

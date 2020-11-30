import unittest

from infracheck.Plugin import Plugin
from infracheck.PluginManager import PluginManager


class PluginTest(unittest.TestCase):
    """
    E-2 - Plugins
    """

    def setUp(self) -> None:
        super().setUp()
        self.plugins = PluginManager()._plugins

    def test_plugin_base_class(self):
        with self.subTest(F"Plugin '{Plugin}' is valid'"):
            self.assertTrue(hasattr(Plugin, '__id__'), F"has a id attribute")
            self.assertTrue(hasattr(Plugin, '__documentation__'), F"has a documentation attribute")
            self.assertTrue(hasattr(Plugin, '__version__'), F"has a version hint attribute")
            self.assertTrue(hasattr(Plugin, 'props'), F"has a props attribute")
            self.assertTrue(hasattr(Plugin, 'json'), F"has modules")
            self.assertTrue(hasattr(Plugin, 'props'), F"has a properties definition")
            self.assertTrue(hasattr(Plugin, '__compatibility__'), F"has a compatibility definition")
            self.assertTrue(hasattr(Plugin, 'setup'), F"has a setup() function")
            self.assertTrue(hasattr(Plugin, 'tear_down'), F"has a tear_down() function")

    def test_integrated_plugins(self):
        for plugin in self.plugins:
            plugin = PluginManager()._get_plugin_instance(plugin)
            with self.subTest(F"Plugin '{plugin.__id__}' is valid'"):
                self.assertTrue(plugin.__id__, F"has a id attribute")
                self.assertTrue(plugin.props, F"has a props attribute")
                self.assertTrue(plugin.json, F"has modules")
                self.assertTrue(plugin.props, F"has a properties definition")
                self.assertTrue(plugin.setup, F"has a setup() function")
                self.assertTrue(plugin.tear_down, F"has a tear_down() function")
                # Optional attributes
                self.assertTrue(hasattr(plugin, '__documentation__'), F"has a documentation attribute")
                self.assertTrue(hasattr(plugin, '__version__'), F"has a version hint attribute")
                self.assertTrue(hasattr(plugin, '__compatibility__'), F"has a compatibility definition")

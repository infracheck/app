import unittest

from infracheck.Module import Module
from infracheck.PluginManager import PluginManager


class ModuleTest(unittest.TestCase):
    """
    E-3 - Modules
    """

    def setUp(self) -> None:
        super().setUp()
        plugins = PluginManager()._plugins
        self.modules = []
        for plugin in plugins:
            plugin = PluginManager()._get_plugin_instance(plugin)
            for module in list(plugin._modules.keys()):
                self.modules = self.modules + [plugin._get_module_instance(module)]
                print(self.modules)

    def test_module_base_class(self):
        with self.subTest(F"Module '{Module}' is valid'"):
            self.assertTrue(hasattr(Module, '__id__'), F"has a id attribute")
            self.assertTrue(hasattr(Module, '__documentation__'), F"has a documentation attribute")
            self.assertTrue(hasattr(Module, '__version__'), F"has a version hint attribute")
            self.assertTrue(hasattr(Module, 'props'), F"has a props attribute")
            self.assertTrue(hasattr(Module, 'json'), F"has a json representation")
            self.assertTrue(hasattr(Module, 'props'), F"has a properties definition")
            self.assertTrue(hasattr(Module, '__compatibility__'), F"has a compatibility definition")
            self.assertTrue(hasattr(Module, 'test'), F"has a test() function")

    def test_integrated_modules(self):
        for module in self.modules:
            with self.subTest(F"Module '{module}' is valid'"):
                self.assertTrue(module.__id__, F"has a id attribute")
                self.assertTrue(module.__documentation__, F"has a documentation attribute")
                self.assertTrue(module.props, F"has a props attribute")
                self.assertTrue(module.json, F"has a json representation")
                self.assertTrue(module.props, F"has a properties definition")
                self.assertTrue(hasattr(module, '__version__'), F"has a version hint attribute")
                self.assertTrue(hasattr(module, '__compatibility__'), F"has a compatibility definition")
                self.assertTrue(hasattr(module, 'test'), F"has a test() function")

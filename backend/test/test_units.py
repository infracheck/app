import unittest
from dataclasses import dataclass

from infracheck.Module import Module
from infracheck.Plugin import Plugin
from infracheck.PluginManager import PluginManager
from infracheck.model.TestInput import TestInput
from infracheck.model.TestResult import TestResult


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


class ValidIODataTest(unittest.TestCase):
    """
    I-1 - Aufbau der Eingabedaten
    I-2 - Aufbau der Ausgabedaten
    """

    def test_valid_input_data(self):
        data = TestInput
        self.assertTrue(type(data), dataclass)
        fields = data.__dataclass_fields__
        self.assertTrue(fields['description'], F"has a description attribute")
        self.assertTrue(fields['plugins'], F"has a plugins attribute")
        self.assertTrue(fields['label'], F"has a label attribute")

    def test_valid_output_data(self):
        data = TestResult
        self.assertTrue(type(data), dataclass)
        fields = data.__dataclass_fields__
        self.assertTrue(fields['id'], F"has a id attribute")
        self.assertTrue(fields['pdf_link'], F"has a pdf_link attribute")
        self.assertTrue(fields['label'], F"has a label attribute")
        self.assertTrue(fields['description'], F"has a description attribute")
        self.assertTrue(fields['success_count'], F"has a success_count attribute")
        self.assertTrue(fields['failure_count'], F"has a failure_count attribute")
        self.assertTrue(fields['total_count'], F"has a total_count attribute")
        self.assertTrue(fields['date'], F"has a date attribute")
        self.assertTrue(fields['message'], F"has a message attribute")
        self.assertTrue(fields['total_count'], F"has a total_count attribute")
        self.assertTrue(fields['plugin_result'], F"has a plugin_result attribute")

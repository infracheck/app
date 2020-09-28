import inspect
import json
import logging
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Any

from infracheck.Module import Module
from infracheck.helper.load_packages import load_packages
from infracheck.model.TestInput import PluginInput
from infracheck.model.TestResult import PluginResult, ModuleResult, ModulePostResult
from infracheck.model.Types import Types

log = logging.getLogger(__name__)


class Plugin(ABC):
    """
    Plugin
    """

    @dataclass
    class props:
        """
        Used to as an interface for plugin properties
        """
        pass

    @property
    def _props_as_json(self):
        """
        Creates a json output of the plugin props that needs to be set
        This is used by the API to give the user information
        about the plugin properties he can configure
        :return:
        """
        attributes = self.props.__dataclass_fields__
        res = {}
        for key, value in attributes.items():
            res[key] = {
                "type": str(value.type),
                "default": value.default
            }
        return res

    def _set_props(self, props: Dict[str, Any]):
        """
        Takes the 'props' dictionary that comes from the API as an input
        and overwrite the Plugin props based on them
        This will be executed before the actual plugin starts test()

        :param props:
        :return:
        """
        for key, value in props.items():
            setattr(self.props, key, value)

    __version__: float = 0.0
    __author__: str = ""

    @property
    def __id__(self):
        """
        The id is defined by the filename of the Plugin object

        :return:
        """
        return os.path.splitext(os.path.basename(inspect.getfile(self.__class__)))[0]

    @property
    def __documentation__(self):
        return inspect.getdoc(self)

    @property
    def json(self) -> json:
        modules = {
            module_id: module_class.json
            for module_id, module_class
            in self._modules.items()
        }
        return {
            "id": self.__id__,
            "author": self.__author__,
            "type": "plugin",
            "documentation": self.__documentation__,
            "version": self.__version__,
            "props": self._props_as_json,
            "modules": modules
        }

    def __init__(self) -> None:
        super().__init__()

        if not self.__id__:
            raise NotImplementedError("id must be set")

        if not self.__documentation__:
            raise NotImplementedError("documentation must be set")

        if len(self._modules.items()) == 0:
            raise NotImplementedError("test modules are missing")

    @property
    def _modules(self) -> Dict[str, Module]:
        plugin_folder_name = os.path.dirname(inspect.getfile(self.__class__)).split('/')[-1]
        modules: List[Module] = load_packages(F"plugins.{plugin_folder_name}.modules", Module)
        return {
            module.__id__: module
            for module in modules
        }

    def _get_module_instance(self, module_id):
        """
        Creates a fresh instance of a plugin by its plugin id

        :param module_id:
        :return:
        """
        try:
            module_instance = self._modules[module_id].__class__()
            return module_instance
        except KeyError:
            raise KeyError(F"Module with id '{module_id}' does not exist in plugin '{self.__id__}'")

    @abstractmethod
    def tear_down(self):
        """
        This method can be implemented by the plugin developer
        to clean up the environment or execute post test actions
        after the test modules were executed
        :return:
        """
        pass

    @abstractmethod
    def setup(self):
        """
        This method can be implemented by the plugin developer
        to run actions and prepare the environment
        before the modules start.
        :return:
        """
        pass

    def test(self, plugin_input: PluginInput) -> PluginResult:
        """
        This is the default test function
        It sets up the test environment, runs the test modules and tear down afterwards
        The setup() and tear_down() should be used by the plugin developers to customize plugin behaviour
        The execute_tests() function will be the same for all plugins
        :param plugin_input:
        :return:
        """
        self.setup()
        result = self._execute_tests(plugin_input)
        self.tear_down()
        return result

    def _execute_tests(self, plugin_input: PluginInput) -> PluginResult:
        """
        This function executes the actual tests
        It deals as deserializer for the input data and spreads it over multiple test modules
        :param plugin_input:
        :return:
        """
        results: List[ModuleResult] = []

        for module_data in plugin_input.modules:
            module = self._get_module_instance(module_data.id)
            module._set_props(module_data.props, self.props)
            module_result: ModulePostResult = module.execute_test()
            module_result.props = self._get_result_props_of(module)
            results.append(module_result)

        return self._serialize_results(results)

    @staticmethod
    def _get_result_props_of(obj: Any) -> Dict[str, Dict[str, str]]:
        """
        The result should contain information about the input data of plugins and modules.
        This function creates that data.
        Because sometimes passwords are send to plugins and modules it is necessary hide their values
        in the test result.

        :param obj: This can be either a module or plugin object
        :return:
        """
        prop_attributes = obj.props.__dataclass_fields__
        result = {}
        for key, value in prop_attributes.items():
            prop_type = str(value.type)
            prop_value = getattr(obj.props, key)

            # If the input is a password -> Hide it's value
            if prop_type == Types.Password:
                prop_value = "************"
            result[key] = {
                "type": prop_type,
                "value": prop_value
            }
        return result

    def _serialize_results(self, module_results: List[ModuleResult]) -> PluginResult:
        """
        Results can come from various modules as a list of ModuleResults
        They need to be serialized before into one object before send back
        to the PluginManager.

        :param module_results:
        :return:
        """
        return PluginResult(
            message=F"{self.__id__}@{self.__version__} complete with failure_count: "
                    F"{sum(not module.result_successful for module in module_results)}",
            success_count=sum(module.result_successful for module in module_results),
            failure_count=sum(not module.result_successful for module in module_results),
            total_count=len(module_results),
            plugin_name=self.__id__,
            module_result=[result for result in module_results],
            props=self._get_result_props_of(self),
            plugin_version=self.__version__
        )

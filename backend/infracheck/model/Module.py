import inspect
import json
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict

from infracheck.model.TestResult import ModuleResult


class Module(ABC):
    """ A Test module is a single test inside a test set """

    __version__: str

    @dataclass
    class props:
        """
        Used to as an interface for module properties
        """
        pass

    @dataclass
    class plugin_props:
        """
        Used to as an interface for plugin properties
        """
        pass

    @property
    def _props_as_json(self):
        """
        Creates a json output of the plugin props
        This is used by the API
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

    @property
    def __id__(self):
        return os.path.splitext(os.path.basename(inspect.getfile(self.__class__)))[0]

    @property
    def __documentation__(self):
        return inspect.getdoc(self)

    @property
    def json(self) -> json:
        return {
            "documentation": self.__documentation__,
            "version": self.__version__,
            "props": self._props_as_json
        }

    def __init__(self) -> None:
        super().__init__()
        if not self.__id__:
            raise NotImplementedError("id must be set")

        if not self.__documentation__:
            raise NotImplementedError("documentation must be set")

    @abstractmethod
    def test(self) -> ModuleResult:
        """
        This should be implemented for each module individually
        :return:
        """
        raise NotImplementedError

    def _set_props(self, module_props: Dict[str, Any], plugin_props: Any):
        """
        Takes the 'props' dictionary that comes from the API as an input
        and overwrite the module props based on them
        This will be executed before the actual module test starts.

        Additionally the global plugin props will be set inside the modules as well.

        :param module_props:
        :return:
        """
        for key, value in module_props.items():
            setattr(self.props, key, value)

        # Pass all plugin props to the modules
        self.plugin_props = plugin_props

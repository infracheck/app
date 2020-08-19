import logging
from abc import abstractmethod, ABC
from typing import List, Dict

from infracheck.helper.load_packages import load_packages
from infracheck.model.IModule import IModule
from infracheck.model.IParam import IParam
from infracheck.model.ITestData import IPluginData
from infracheck.model.ITestResult import IPluginResult

log = logging.getLogger(__name__)


class IPlugin(ABC):
    modules: List[IModule] = []

    @property
    def id(self) -> str:
        raise NotImplementedError

    @property
    def version(self) -> float:
        raise NotImplementedError

    @property
    def documentation(self) -> str:
        raise NotImplementedError

    @property
    def params(self) -> Dict[str, IParam]:
        raise NotImplementedError

    def __init__(self) -> None:
        self.reload_modules()

    @abstractmethod
    def test(self, plugin_data: IPluginData) -> IPluginResult:
        raise NotImplementedError

    def reload_modules(self):
        """ Reloads all available modules from ./modules folder """
        self.modules = load_packages(F"plugins.{self.id}.modules", IModule)

    def get_module_by_id(self, module_id: str):
        """
        Returns the test module based on its id
        :param module_id:
        :return:
        """
        return list(filter(lambda module: module.id == module_id, self.modules))[0]

    def list_modules(self):
        return list(
            {
                "id": x.id,
                "documentation": x.documentation,
                "params": x.params,
                "version": x.version,
                "code": x.code
            }
            for x in self.modules)

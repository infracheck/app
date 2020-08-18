import logging
from abc import ABCMeta
from typing import List

from infracheck.helper.load_packages import load_packages
from infracheck.model.ITestData import IPluginData, IGeneralPluginData
from infracheck.model.ITestModule import ITestModule
from infracheck.model.ITestResult import IPluginResult

log = logging.getLogger(__name__)


class IPlugin(object):
    __metaclass__ = ABCMeta
    modules: List[ITestModule]
    id: str
    version: float
    documentation: str
    data: IGeneralPluginData = {}

    def __init__(self) -> None:
        self.reload_modules()

    def __str__(self) -> str:
        return self.id

    # noinspection PyTypeChecker
    def test(self, data: IPluginData) -> IPluginResult:
        pass

    def reload_modules(self):
        """ Reloads all available modules from ./modules folder """
        self.modules = load_packages(F"plugins.{self.id}.modules", ITestModule)

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
                "fields": x.fields,
                "version": x.version,
                "code": x.code
            }
            for x in self.modules)

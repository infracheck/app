import typing as t
from abc import ABCMeta, abstractmethod
from typing import TypedDict, List

from infracheck.helper.load_packages import load_packages
from infracheck.model.ITestModule import ITestModule


class FieldData(TypedDict):
    """ This is the data for a single field in a test module

    """
    id: str
    content: str


class TestData(TypedDict):
    """ This is the data for a single test module
    """
    id: str
    fields: List[FieldData]


class PluginData(TypedDict):
    """ This data is delivered to a plugin during test launch
    """
    test_set: List[TestData]


class TestResult(t.TypedDict):
    succeeded: int
    failures: int
    errors: int
    total: int
    message: str
    data: t.Any


class IPlugin(object):
    __metaclass__ = ABCMeta
    modules: List[ITestModule]
    id: str
    version: str
    documentation: str
    package_name: str

    def __str__(self) -> str:
        return self.id

    @abstractmethod
    def test(self, data: PluginData) -> TestResult:
        raise NotImplementedError

    def reload_modules(self):
        """ Reloads all available modules from ./modules folder """
        self.modules = load_packages(F"plugins.{self.package_name}.modules", ITestModule)

    def list_modules(self):
        res = list(map(lambda x: {
            "id": x.id,
            "version": x.version,
            "documentation": x.documentation,
            "fields": x.fields
        }, self.modules))

        return res

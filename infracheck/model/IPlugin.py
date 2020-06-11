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
    seen_paths = []

    def __init__(self):
        self.modules = []
        self.id = 'BasePlugin'
        self.version = '0.1'
        self.package_name = 'UNSET'
        self.documentation = 'This is some documentation'

    def __str__(self) -> str:
        return self.id

    @abstractmethod
    def test(self, data: PluginData) -> TestResult:
        raise NotImplementedError

    def reload_modules(self, package_name: str):
        """ Reloads all available modules from ./modules folder """
        self.modules = load_packages(package_name, ITestModule)

import logging
import subprocess
import typing as t
from abc import ABCMeta, abstractmethod
from typing import TypedDict, List

from infracheck.helper.load_packages import load_packages
from infracheck.model.ITestModule import ITestModule

log = logging.getLogger(__name__)


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
    requirements: List[str]

    def __init__(self) -> None:
        with open(F"plugins/{self.package_name}/requirements.txt") as requirements_file:
            self.requirements = requirements_file.read().splitlines()
        self.install_packages()

    def __str__(self) -> str:
        return self.id

    def install_packages(self):
        for package in self.requirements:
            log.info(F"|---- {package}")
            try:
                subprocess.Popen(['pip', 'install', package], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            except Exception as e:
                log.error(e)

    @abstractmethod
    def test(self, data: PluginData) -> TestResult:
        raise NotImplementedError

    def reload_modules(self):
        """ Reloads all available modules from ./modules folder """
        self.modules = load_packages(F"plugins.{self.package_name}.modules", ITestModule)

    def list_modules(self):
        return list(
            {
                "id": x.id,
                "version": x.version,
                "documentation": x.documentation,
                "fields": x.fields
            }
            for x in self.modules)

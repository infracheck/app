import logging
import subprocess
import typing as t
from abc import ABCMeta
from typing import List

from infracheck.helper.load_packages import load_packages
from infracheck.model.ITestData import IPluginData, IGeneralPluginData
from infracheck.model.ITestModule import ITestModule

log = logging.getLogger(__name__)


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
    name: str
    documentation: str
    package_name: str
    data: IGeneralPluginData = {}

    def __init__(self) -> None:
        with open(F"plugins/{self.package_name}/requirements.txt") as requirements_file:
            requirements = requirements_file.read().splitlines()
            for package in requirements:
                log.info(F"|---- {package}")
                try:
                    subprocess.Popen(['pip', 'install', package], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                except Exception as e:
                    log.error(e)

    def __str__(self) -> str:
        return self.name

    # noinspection PyTypeChecker
    def test(self, data: IPluginData) -> TestResult:
        self.data = data['data']
        pass

    def reload_modules(self):
        """ Reloads all available modules from ./modules folder """
        self.modules = load_packages(F"plugins.{self.package_name}.modules", ITestModule)

    def list_modules(self):
        return list(
            {
                "name": x.name,
                "documentation": x.documentation,
                "fields": x.fields
            }
            for x in self.modules)

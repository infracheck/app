import logging
import subprocess
from abc import ABCMeta
from typing import List

from infracheck.helper.load_packages import load_packages
from infracheck.model.ITestData import IPluginData, IGeneralPluginData
from infracheck.model.ITestModule import ITestModule
from infracheck.model.ITestResult import TestResult

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
        with open(F"plugins/{self.id}/requirements.txt") as requirements_file:
            requirements = requirements_file.read().splitlines()
            for package in requirements:
                log.info(F"|---- {package}")
                try:
                    subprocess.Popen(['pip', 'install', package], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                except Exception as e:
                    log.error(e)

    def __str__(self) -> str:
        return self.id

    # noinspection PyTypeChecker
    def test(self, data: IPluginData) -> TestResult:
        self.data = data['data']
        pass

    def reload_modules(self):
        """ Reloads all available modules from ./modules folder """
        self.modules = load_packages(F"plugins.{self.id}.modules", ITestModule)

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

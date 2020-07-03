from typing import List

import xml.dom.minidom

from infracheck.model.DataTypes import DataTypes
from infracheck.model.IPlugin import IPlugin
from infracheck.model.ITestData import IPluginData, IModuleData, IGeneralPluginData
from infracheck.model.ITestResult import TestResult

class TestInfraPluginData(IGeneralPluginData):
    hosts: List[str]
    username: str
    password: str


class DemoPlugin(IPlugin):
    id = 'demo_plugin'
    documentation = """
    This Testinfra plugins enable you to run customized code snippets using the testinfra framework
    """
    data: TestInfraPluginData = {
        "hosts": DataTypes.TextList,
        "username": DataTypes.Text,
        "target_os": DataTypes.Text,
        "password": DataTypes.Text,
        "port": DataTypes.Number
    }

    def test(self, _data: IPluginData) -> TestResult:
        return {"PLACEHOLDER": "PLACEHOLDER"}

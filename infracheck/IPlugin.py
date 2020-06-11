import typing as t
from abc import ABCMeta, abstractmethod
from enum import Enum
from typing import TypedDict, List


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


class FieldType(Enum):
    Text = "string"
    Number = "number"
    List = "array"
    Dict = "dict"


class ITestModule(object):
    __metaclass__ = ABCMeta

    documentation: t.Any
    id: str
    version: str
    fields: t.Dict[str, FieldType]

    def __init__(self):
        self.fields = {}
        self.id = 'BasePlugin'
        self.version = '0.1'
        self.documentation = 'This is some documentation'


class IPlugin(object):
    __metaclass__ = ABCMeta
    modules: List[ITestModule]
    id: str
    version: str
    documentation: str

    def __init__(self):
        self.modules = []
        self.id = 'BasePlugin'
        self.version = '0.1'
        self.documentation = 'This is some documentation'

    def __str__(self) -> str:
        return self.id

    @abstractmethod
    def test(self, data: PluginData) -> TestResult: raise NotImplementedError

import typing as t
from abc import ABCMeta, abstractmethod
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


class Plugin(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.id = 'BasePlugin'
        self.version = '0.1'

    def __str__(self) -> str:
        return self.id

    @abstractmethod
    def test(self, data: PluginData) -> TestResult: raise NotImplementedError

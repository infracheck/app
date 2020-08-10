import inspect
import typing as t
from abc import ABCMeta

from infracheck.model.DataTypes import DataTypes


class ITestModule(object):
    """ A Test module is a single test inside a test set """
    __metaclass__ = ABCMeta
    documentation: t.Any
    id: str
    version: float
    fields: t.Dict[str, DataTypes]

    @property
    def code(self):
        return inspect.getsource(self.test)

    def test(self):
        pass

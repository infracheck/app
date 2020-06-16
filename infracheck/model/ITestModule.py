import typing as t
from abc import ABCMeta

from infracheck.model.FieldTypes import DataTypes


class ITestModule(object):
    """ A Test module is a single test inside a test set """
    __metaclass__ = ABCMeta
    documentation: t.Any
    name: str
    version: str
    fields: t.Dict[str, DataTypes]

    def __str__(self) -> str:
        return F"{self.name}:{self.version}"

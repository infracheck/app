import typing as t
from abc import ABCMeta

from infracheck.model.FieldTypes import FieldType


class ITestModule(object):
    """ A Test module is a single test inside a test set """
    __metaclass__ = ABCMeta
    documentation: t.Any
    id: str
    version: str
    fields: t.Dict[str, FieldType]

    def __str__(self) -> str:
        return F"{self.id}:{self.version}"

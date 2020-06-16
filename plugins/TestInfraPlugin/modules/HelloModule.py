import pytest

from infracheck.model.FieldTypes import FieldType
from infracheck.model.ITestModule import ITestModule


class HelloModule(ITestModule):
    id = "HelloModule"
    version = "1.0"
    documentation = """
    Some stupid hello stuff
    """
    fields = {
        "number": str(FieldType.Number)
    }


    def test(number):
        assert number == 0

from infracheck.model.FieldTypes import DataTypes
from infracheck.model.ITestModule import ITestModule


class HelloModule(ITestModule):
    name = "HelloModule"
    version = "1.0"
    documentation = """
    Some stupid hello stuff
    """
    fields = {
        "number": str(DataTypes.Number.value)
    }

    def test(number):
        assert number == 0

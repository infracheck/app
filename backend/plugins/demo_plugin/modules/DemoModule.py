
from infracheck.model.DataTypes import DataTypes
from infracheck.model.ITestModule import ITestModule


class DemoModule(ITestModule):
    id = "demo_module"
    documentation = """
    Check is a address is reachable
    """
    fields = {
        "url": DataTypes.Text
    }

    def test(self, data):
        return data

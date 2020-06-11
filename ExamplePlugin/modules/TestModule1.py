from infracheck.model.FieldTypes import FieldType
from infracheck.model.ITestModule import ITestModule


class ExampleModule(ITestModule):
    id = "FIRST"
    version = "1.0"
    documentation = "FIRST"
    fields = {
        "FIRST_1": str(FieldType.Number),
        "FIRST_2": str(FieldType.Text)
    }

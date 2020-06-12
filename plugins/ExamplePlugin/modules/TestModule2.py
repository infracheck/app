from infracheck.model.FieldTypes import FieldType
from infracheck.model.ITestModule import ITestModule


class ExampleModule(ITestModule):
    id = "SECOND"
    version = "1.0"
    documentation = "SECOND"
    fields = {
        "SECOND_1": str(FieldType.Number),
        "SECOND_2": str(FieldType.Number)
    }

from infracheck.model.FieldTypes import FieldType
from infracheck.model.ITestModule import ITestModule


class ExampleModule(ITestModule):
    id = "ExampleModule"
    version = "1.0"
    documentation = "Example documentation"
    fields = {
        "field_1": FieldType.Number,
        "field_2": FieldType.Text
    }

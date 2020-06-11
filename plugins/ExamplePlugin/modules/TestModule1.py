from infracheck.IPlugin import ITestModule, FieldType


class ExampleModule(ITestModule):
    id = "ExampleModule"
    version = "1.0"
    documentation = "Example documentation"
    fields = {
        "field_1": FieldType.Number,
        "field_2": FieldType.Text
    }

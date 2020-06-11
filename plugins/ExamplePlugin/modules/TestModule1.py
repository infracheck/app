from infracheck.IPlugin import ITestModule, FieldType


class ExampleModule(ITestModule):
    def __init__(self):
        super().__init__()
        self.id = "ExampleModule"
        self.version = "1.0"
        self.documentation = "Example documentation"
        self.fields = {
            "field_1": FieldType.Number,
            "field_2": FieldType.Text
        }

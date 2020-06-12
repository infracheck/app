from infracheck.model.FieldTypes import FieldType
from infracheck.model.ITestModule import ITestModule


class RegexModule(ITestModule):
    id = "RegexModule"
    version = "1.0"
    documentation = """
    This test performs a regex comparison
    """
    fields = {
        "FIRST_1": str(FieldType.Number),
        "FIRST_2": str(FieldType.Text)
    }

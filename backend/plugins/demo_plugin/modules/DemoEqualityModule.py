from infracheck.model.DataTypes import DataTypes
from infracheck.model.ITestModule import ITestModule
from infracheck.model.ITestResult import IModuleResult


class DemoEqualityModule(ITestModule):
    id = "equality_check"
    version = 0.1
    documentation = """
Check equality of two inputs
============

## Description
Write a short description what your test is doing.
        
## Examples
```
# Write some examples, how the test data could look like.
{
    "example_key": ['to', 'store', 'useless', 'stuff', 'in', 'this', 'list'],
    "another_key": ['google.de', 'proficom.de'],
}
```

## Plugin Version
0.1.0

[Use semantic versioning here](https://semver.org/)

## Author
Write who to blame for bad test (or celebrate for good ones).
Martin Welcker <mwelcker@proficom.de>
"""
    fields = {
        "number1": DataTypes.Number,
        "number2": DataTypes.Number
    }

    def test(self) -> IModuleResult:
        equal = self.fields['input1'] == self.fields['input2']
        result: IModuleResult = {
            "module_name": self.id,
            "module_version": self.version,
            "fields": self.fields,
            "success": equal,
            "message": "They are equal" if equal else "They are not equal",
        }
        return result

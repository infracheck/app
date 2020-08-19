from typing import Dict

from infracheck.model.DataTypes import DataTypes
from infracheck.model.IModule import IModule
from infracheck.model.IParam import IParam
from infracheck.model.ITestResult import IModuleResult


class DemoEqualityModule(IModule):
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
    params: Dict[str, IParam] = {
        "number1": {
            "type": DataTypes.Number,
            "value": ''
        },
        "number2": {
            "type": DataTypes.Password,
            "value": ''
        }
    }

    def test(self) -> IModuleResult:
        equal = self.params['number1']['value'] == self.params['number2']['value']
        result: IModuleResult = {
            "module_name": self.id,
            "module_version": self.version,
            "params": self.params,
            "is_successful": equal,
            "message": "They are equal" if equal else "They are not equal",
        }
        return result

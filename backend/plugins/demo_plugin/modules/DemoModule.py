
from infracheck.model.DataTypes import DataTypes
from infracheck.model.ITestModule import ITestModule


class DemoModule(ITestModule):
    id = "demo_module"
    documentation = """
Name of your test
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
        "url": DataTypes.Text
    }

    def test(self, data):
        return data

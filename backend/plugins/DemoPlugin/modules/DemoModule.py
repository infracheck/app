from infracheck.Module import Module
from infracheck.model.TestResult import ModuleResult
from infracheck.model.Types import Types


class DemoModule(Module):
    """
Modules contain the actual test methods and their functionality.
They take input data and run tests based on that.
Each module needs to implement a `test()` method for that, that returns a `ModuleResult` object.

## Input props
Modules can receive input data in two different ways:

**Local module data**
This data is defined inside the `props` classes in each module. The data there is received by the declaring module only.
From the module perspective you cann call it local data.
It is available only inside the module and only if it was set by the user.
For example, the module defines the following `props` class:
```python
class props:
    local_var: Types.Text = "Hello World"
    second_local_var: Types.Password = ""
```
You can access it using the `props` parameter:
```python
print(self.props.local_var)
print(self.props.second_local_var)
```

**Global data from the plugin**
Data that is defined inside the `props` class of the plugin is available in every module of the plugin.
For example, the plugin defines the following `props` class:
```python
class props:
    host: Types.Text = "localhost"
    port: Types.Number = 22
```
You can now use access it's data inside the module using the `plugin_props` variable:
```python
print(self.plugin_props.host)
print(self.plugin_props.port)
```

## Test Result
The module creates the actual result of the test.
Because result data from various modules needs to be serialized, it is necessary to implement a standardized module output, the `infracheck.model.TestResult`.
It contains three properties:

**result_successful**
A `Boolean`, that indicates if the test was successful.
```python
# examples
result_successful=true
result_successful=false
result_successful= output1 == output2
```

**result_message**
A custom message that each module developer can choose individually.
It should contain textual information about failing and succeeding tests.
```python
# examples
result_successful="Test was successful"
result_successful=F"{'Test was successful' if successful else 'Test failed'}"
result_message="They are equal" if equal else "They are not equal"
```

**result_data**
Result data is an additional data object. It can be used to store additional information in a `dict`.
Sometimes if your modules are more complex, it is necessary to provide deeper test results.
```python
# examples
result_data={"difference_between_numbers": self.props.input2 - self.props.input1}
result_data = {
    "is_enabled": service.is_enabled,
    "is_running": service.is_running
}
```
"""
    __version__ = 0.1
    __author__ = "Martin Welcker <mwelcker@proficom.de>"

    class props:
        input1: Types.Number = -1
        input2: Types.Number = -1

    def test(self) -> ModuleResult:
        """
        :return:
        """
        print(F"Access global plugin parameters: {self.plugin_props.new_global_variable}")
        print(F"Access module parameters: {self.props.input1}")

        equal = self.props.input1 == self.props.input2
        return ModuleResult(
            result_successful=equal,
            result_message="They are equal" if equal else "They are not equal",
            result_data={"difference_between_numbers": self.props.input2 - self.props.input1}
        )

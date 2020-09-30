from dataclasses import dataclass

from infracheck.Plugin import Plugin
from infracheck.model.Types import Types


class DemoPlugin(Plugin):
    """
> Please don't use this plugin for real testing
> This plugin deals as an example for further plugin development.
# Plugins
Plugins in **InfraCheck** need to be stored inside a sub folder in the `/plugins` folder.
The name of the sub folder can be chosen as wanted, because it does not matter for **InfraCheck** functionality.
Every plugin needs to inherit from the `infracheck.Plugin` class, to work properly.

**Options as plugin creator**

## Plugin meta properties
Plugins have of the following properties that can be set optionally:
* `__version__` (optional)
* `__documentation__` (optional)
* `__author__` (optional)
* `__id__` (generated automatically from the classname if not explicitly set)
All these properties can be set by a plugin creator, though it is not necessary, because they are optional
or generated automatically, like the `__id__`.

**Documentation**
This documentation part will be parsed and used by the API and the frontend.
This is just one o two ways to write a description for your plugins.
An alternative would be to store it inside a class variable called `__documentation__`.

_Example_:
```python
__documentation__="This can contain markdown as well"
```

## Input props
Each plugin should contain a inner data class, called `props`.
It deals as an interface for possible plugin input.
Those can be used inside each module of the plugin, or inside the plugin itself.
For example, the **TestInfraPlugin** runs tests on remote hosts.
It needs a host and its credentials as input.
Example:
```
@dataclass
    class props:
        host: Types.Text = "localhost"
        port: Types.Number = 22
```

### Input types
Supported types are defined inside the `infracheck.model.Types` and include:

| Id         | Label              | Python type | JS type |
|------------|--------------------|-------------|---------|
| Text       | "Type.String"      |             |         |
| Number     | "Type.Number"      |             |         |
| Boolean    | "Type.Boolean"     |             |         |
| TextList   | "Type.StringArray" |             |         |
| NumberList | "Type.NumberArray" |             |         |
| Password   | "Type.Password"    |             |         |

## Plugin Hooks
The lifecycle of all plugins looks quite equal.
Based on the test input, they are executed and run through the following steps:
0. `init()`
1. `setup()`
2. `test()`
3. `teardown()`
### 1. Init
The plugin manager starts the initialization of a plugin if a testset uses it.
The input values from the test set will be set inside the plugin and all the modules,
that should be executed. The Input is formatted as JSON and could look like:
```json
{   "id": "TestInfraPlugin",
    "props": {
        "host_address": "localhost",
        "username": "",
        "port": 22
        },
    "modules": [...]}
```
### Setup
The `setup()` method is optional and can be implemented by the plugin developer, to set up the test environment.
Operations based on `props` can be executed here and additional global `props` can be set, for usage in the modules.

```
def setup(self):
    self.props.new_global_variable = "I am a new global variable to be used inside the modules"
    print("Do anything you want here")
```

### Test
During the test step, modules are executed based on the user input.
The `modules` section inside the input JSON contains a list of modules with their input data.
example:
```json
[{
  "id": "AddressReachable",
  "props": {
     "url": "google.de"
   }
}, ... ]
```
Item per item, each module executes it's test based on the data and returns it's test result.
Read more about modules in the `DemoModule`.

### Teardown
The `teardown` is the opposite of the `setup` method.
If you need to clean up your environment after testing, you can do it here.
```
def tear_down(self):
    database.close_connection()
    print("Do anything you want here")
```
"""
    __version__ = 0.5
    __author__ = "Martin Welcker"

    @dataclass
    class props:
        """
        Definition of Plugin input
        These props are available inside the Plugin functions and their modules
        These are exposed to the API and should be configured by the user,
        when he launches tests.
        Please define the input type, using the Types available.
         -> Type.Text, Type.Pass
        """
        global_text_list: Types.TextList = "['some','list']"
        global_number_list: Types.NumberList = "[1,2,3]"
        global_number: Types.Number = 200
        global_text: Types.Text = 'Hello World'
        global_secret: Types.Password = 'Start123'
        global_boolean: Types.Boolean = True


    """
    Define as many private attributes as you need.
    They don't get exposed
    """

    private_value: str = "I am a private attribute"

    def setup(self):
        """
        This method is executed before the test modules
        You can setup your environment, databases, ssh connection,
        or whatever you need before the actual tests start
        :return:
        """

        # You can pass new variables to the modules by adding them to the 'props' object
        # This way, they don't get exposed to the API
        self.props.new_global_variable = "I am a new plugin variable"
        print("no after action")

    def tear_down(self):
        """
        You can do some post processing of your test results here,
        or clean up your test environment
        :return:
        """
        print("no before action")

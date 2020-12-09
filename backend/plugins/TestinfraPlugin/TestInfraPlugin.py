from infracheck.Plugin import Plugin
from infracheck.model.Types import Types
from plugins.TestinfraPlugin.TestInfraConnector import Connection


class TestInfraPlugin(Plugin):
    """
This plugin is a wrapper for the python framework [testinfra](https://testinfra.readthedocs.io/).
With Testinfra you can write unit tests in Python to test actual state of
your servers configured by management tools like Salt, Ansible, Puppet, Chef and so on. Testinfra aims to be a
Serverspec equivalent in python and is written as a plugin to the powerful Pytest test engine.
This plugin implements various [testinfra modules](https://testinfra.readthedocs.io/en/latest/modules.html).

## Connection Backends
Testinfra comes with several connections backends for remote command execution. This plugin features the following:
* `ssh` for any linux distribution with sshd enabled
* `winrm` for tests on windows distributions
* `local` for tests on this server (_use it for debugging if no remote server is available_)

To support tests on large clusters, you can provide a list of hosts as input, like `["192.168.1.1", "myhost.de"]`.
The credentials, `username`, `password` and `port` should be the same for every host.
If you want to test hosts with different credentials, you can add this plugin twice to your testset.

## Properties
The following input properties can be set when launching the plugin: **`host_address`** List of hosts to test.
It can be any host address, like `["localhost"]`,  ip adresses (`["192.168.1.1"]`), dns names `["rpi01"]` or domains `["google.de"]`.
If you choose to test `['localhost']`, the test will run on the server itself and though no `username`, `os`, `password` and `port` needs to be set.

**`os`**
The `os` can either be `"linux"` oder `"windows"`. This decides, which connection backend will be used, `winrm` or `ssh`.

**`username`**
The username is the nae of the user, that performs the `ssh` or `winrm` connection.
Make sure, that this user has the needed privileges.

**`password`**
The password of the selected user. It is internally handeld as a input of type `type.password` and not `type.text` like other text properties.
Though it won't get saved inside the database and in any test result.

**`port`**
This is the connection port that should be used for the `winrm` or `ssh` connection.
The default port for `ssh` is `22`. For `winrm` it is `5985`.

## Setup() and Teardown()
During setup() the plugin establishes your connection. This is done with `paramiko`.
Connections to windows systems with `winrm` are performed with username and password as inputs.
For `ssh`, `paramiko` requires a key based authorization.
For that the plugin creates a ssh key and registers it at the client using `ssh-copy-id`.
During teardown(), if the tests are completed, the key will be deleted on the host.

## Testinfra <-> Infracheck comparison
With a wide variete of modules supported, you can save a lot of effort writing your infrastructure tests.
Take the following `testinfra` code:
```python
host = testinfra.get_host("local://")
is_resolvable = host.addr("google.de").is_resolvable
is_reachable = host.addr("google.de").is_reachable

if is_resolvable == False or is_reachable == False:
    result_successful = False
    result_message = F"Test failed"
else:
    result_successful = True
    result_message = F"Test succeeded"
```
and compare it to the `infracheck` input:
```json
{"id": "AddressReachable",
"props": {
    "url": "google.de"
}}
```
    """
    __version__ = 0.5
    __author__ = "Martin Welcker <mwelcker@proficom.de>"
    __compatibility__ = "Linux, Windows(partly)"

    class props:
        host_address: Types.TextList = ["localhost"]
        username: Types.Text = ""
        os: Types.Text = "linux"
        password: Types.Password = ""
        port: Types.Number = 22

    def setup(self):
        self.props.connections = []  # List of hosts

        for address in self.props.host_address:
            self.props.connections.append(
                Connection(
                    self.props.username, address,
                    self.props.password, self.props.port,
                    self.props.os).host
            )

    def tear_down(self):
        pass

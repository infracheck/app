from infracheck.Module import Module
from infracheck.model.TestResult import ModuleResult
from infracheck.model.Types import Types


class CheckCommandOutput(Module):
    """
Runs two different commands on the host and checks if their stdouts are equal.
This can be used for comparison operations as well, for example:
```json
command1 = "echo username"
command2 = "whoami"
```

## Properties
* `command1`: First command to launch on the remote console of the host
* `command2`: Second command

## To do
* `exit_status`: Check for exit_status (rc)
* `stderr`: Check for stderr
    """
    __version__ = 0.1
    __author__ = "Martin Welcker <mwelcker@proficom.de>"
    __compatibility__ = "Linux, Windows"

    class props:
        command1: Types.Text = "echo Hello"
        command2: Types.Text = "echo Hello"

    def test(self) -> ModuleResult:
        message = ''
        successful = True
        res_data = {}

        cmd1 = self.props.command1
        cmd2 = self.props.command2

        for connection in self.plugin_props.connections:
            host = connection.host
            output_cmd1 = host.run(cmd1).stdout
            output_cmd2 = host.run(cmd2).stdout

            if output_cmd1 != output_cmd2:
                successful = False
                message += F"'{connection.name}' -'{output_cmd1}'{'==' if output_cmd1 == output_cmd2 else '!='}'{output_cmd2}' | "

            res_data[connection.name] = {
                "Output Command1": output_cmd1,
                "Output Command2": output_cmd2
            }

        return ModuleResult(
            result_successful=successful,
            result_message='Test successful' if successful else message,
            result_data=res_data
        )

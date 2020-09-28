from dataclasses import dataclass

from infracheck.Module import Module
from infracheck.model.TestResult import ModuleResult
from infracheck.model.Types import Types


class OSSpecs(Module):
    """
    Martin Welcker <mwelcker@proficom.de>
    """
    __version__ = 0.1

    @dataclass
    class props:
        command1: Types.Text = "echo Hello"
        command2: Types.Text = "echo Hello"

    def test(self) -> ModuleResult:
        cmd1 = self.props.command1
        cmd2 = self.props.command2

        output_cmd1 = self.plugin_props.host.run(cmd1).stdout
        output_cmd2 = self.plugin_props.host.run(cmd2).stdout

        return ModuleResult(
            result_successful=output_cmd1 == output_cmd2,
            result_message=F"<Output>: '{output_cmd1}'"
                           F"{'==' if output_cmd1 == output_cmd2 else '!='}"
                           F"<Output>: '{output_cmd2}'",
            result_data={
                "Output Command1": output_cmd1,
                "Output Command2": output_cmd2
            }
        )

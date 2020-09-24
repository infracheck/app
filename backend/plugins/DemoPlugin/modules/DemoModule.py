from dataclasses import dataclass

from infracheck.model.Module import Module
from infracheck.model.TestResult import ModuleResult
from infracheck.model.Types import Types


class DemoModule(Module):
    """
    #Check equality of two inputs
    ============
    ## Description
    Write a short description what your test is doing.

    ## Author
    Martin Welcker <mwelcker@proficom.de>
    """
    __version__ = 0.1

    @dataclass
    class props:
        input1: Types.Number = -1
        input2: Types.Number = -1

    def test(self) -> ModuleResult:
        """
        :return:
        """
        print(F"Access global plugin parameters: {self.plugin_props.rofl}")
        print(F"Access module parameters: {self.props.input1}")

        equal = self.props.input1 == self.props.input2
        return ModuleResult(
            is_successful=equal,
            message="They are equal" if equal else "They are not equal",
            custom_data={"difference_between_numbers": self.props.input2 - self.props.input1}
        )

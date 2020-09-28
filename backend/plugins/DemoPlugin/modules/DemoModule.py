from dataclasses import dataclass

from infracheck.Module import Module
from infracheck.model.TestResult import ModuleResult
from infracheck.model.Types import Types


class DemoModule(Module):
    """
    Write a short description what your test is doing.
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
        print(F"Access global plugin parameters: {self.plugin_props.new_global_variable}")
        print(F"Access module parameters: {self.props.input1}")

        equal = self.props.input1 == self.props.input2
        return ModuleResult(
            result_successful=equal,
            result_message="They are equal" if equal else "They are not equal",
            result_data={"difference_between_numbers": self.props.input2 - self.props.input1}
        )

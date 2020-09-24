from dataclasses import dataclass
from unittest import TestCase

import testinfra

from infracheck.Module import Module
from infracheck.model.TestResult import ModuleResult
from infracheck.model.Types import Types


class OSSpecs(Module, TestCase):
    """
    ## Author
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

        with self.subTest("Type"):
            self.assertTrue(
                self.plugin_props.host.run(cmd1).stdout == self.plugin_props.host.run(cmd2).stdout,
                F"Response dont match {self.plugin_props.host.run(cmd1).stdout} != {self.plugin_props.host.run(cmd2).stdout}"
            )
        return ModuleResult()

from typing import Dict
from unittest import TestCase

import testinfra

from infracheck.model.Types import Types
from infracheck.model.Module import Module
from infracheck.model.Property import Property


class OSSpecs(Module, TestCase):
    id = "compare_commands"
    version = 0.1
    documentation = """

## Plugin Version
0.0.1

## Author
Martin Welcker <mwelcker@proficom.de>
"""
    params: Dict[str, Property] = {
        "command1": {
            "type": Types.Text,
            "value": ''
        },
        "command2": {
            "type": Types.Text,
            "value": ''
        }
    }
    host = testinfra.get_host("local://")

    def test(self):
        cmd1 = self.params['command1']['value']
        cmd2 = self.params['command2']['value']

        with self.subTest("Type"):
            self.assertTrue(
                self.host.run(cmd1).stdout == self.host.run(cmd2).stdout,
                F"Response dont match {self.host.run(cmd1).stdout} != {self.host.run(cmd2).stdout}"
            )

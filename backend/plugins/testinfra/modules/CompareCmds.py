from typing import Dict
from unittest import TestCase

import testinfra

from infracheck.model.DataTypes import DataTypes
from infracheck.model.IModule import IModule
from infracheck.model.IParam import IParam


class OSSpecs(IModule, TestCase):
    id = "compare_commands"
    version = 0.1
    documentation = """

## Plugin Version
0.0.1

## Author
Martin Welcker <mwelcker@proficom.de>
"""
    params: Dict[str, IParam] = {
        "command1": {
            "type": DataTypes.Text,
            "value": ''
        },
        "command2": {
            "type": DataTypes.Text,
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

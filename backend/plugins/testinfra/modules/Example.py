from typing import Any, Dict
from unittest import TestCase

import testinfra

from infracheck.model.DataTypes import DataTypes
from infracheck.model.IModule import IModule
from infracheck.model.IParam import IParam


class Example(IModule, TestCase):
    id = 'hello_world'
    version = 0.1
    documentation = 'ROFL'
    params: Dict[str, IParam] = {
        "number": {
            "value": 0,
            "type": DataTypes.Number
        }
    }
    host = testinfra.get_host("local://")

    def test(self) -> Any:
        with self.subTest('Is smaller then 2'):
            self.assertLess(self.params['number']['value'], 2)
        with self.subTest('Is bigger then 1'):
            self.assertGreater(self.params['number']['value'], 1)

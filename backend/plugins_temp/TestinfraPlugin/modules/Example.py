from typing import Any, Dict
from unittest import TestCase

import testinfra

from infracheck.model.Types import Types
from infracheck.model.Module import Module
from infracheck.model.Property import Property


class Example(Module, TestCase):
    id = 'hello_world'
    version = 0.1
    documentation = 'ROFL'
    params: Dict[str, Property] = {
        "number": {
            "value": 0,
            "type": Types.Number
        }
    }
    host = testinfra.get_host("local://")

    def test(self) -> Any:
        with self.subTest('Is smaller then 2'):
            self.assertLess(self.params['number']['value'], 2)
        with self.subTest('Is bigger then 1'):
            self.assertGreater(self.params['number']['value'], 1)

from typing import Dict
from unittest import TestCase

import testinfra

from infracheck.model.DataTypes import DataTypes
from infracheck.model.IModule import IModule
from infracheck.model.IParam import IParam


class AddressReachable(IModule, TestCase):
    id = "address"
    version = 0.1
    documentation = """
    # Is adress reachable [Linux]
---

## Description:
This test checks if a list of hosts is reachable.

[Testinfra Docs](
https://testinfra.readthedocs.io/en/latest/modules.html#testinfra.modules.addr.Addr) 
        
## Examples:
```json
# Checking a list of hosts
{"addr_list": ["google.de", "proficom.de"]}

# Checking for a single hosts
{"addr_list": ["google.de"]}

# Checks for 
{"addr_list": ["192.168.0.10", "127.0.0.1"]}
```

## Plugin Version
0.1.1


## Author
Martin Welcker <mwelcker@proficom.de>
"""

    params: Dict[str, IParam] = {
        "url": {
            "type": DataTypes.Text,
            "value": 'localhost'
        }
    }
    host = testinfra.get_host("local://")

    def test(self):
        addr = self.params['url']['value']

        with self.subTest("Resolvable"):
            self.assertTrue(
                self.host.addr(addr).is_resolvable,
                F"Address {addr} is not resolvable"
            )

        with self.subTest("Reachable"):
            self.assertTrue(
                self.host.addr(addr).is_reachable,
                F"Address {addr} is not resolvable"
            )

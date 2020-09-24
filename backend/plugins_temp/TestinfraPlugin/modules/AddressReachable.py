from typing import Dict
from unittest import TestCase

import testinfra

from infracheck.model.Types import Types
from infracheck.model.Module import Module
from infracheck.model.Property import Property


class AddressReachable(Module, TestCase):
    id = "address"
    version = 0.1
    documentation = """
    # Is address reachable [Linux]
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

    params: Dict[str, Property] = {
        "url": {
            "type": Types.Text,
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

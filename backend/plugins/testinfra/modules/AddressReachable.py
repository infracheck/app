from typing import Dict
from unittest import TestCase

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
    host = None

    def test(self):
        addr = self.params['url']
        curr_addr = self.host.addr(addr)
        assert curr_addr.is_resolvable
        assert curr_addr.is_reachable

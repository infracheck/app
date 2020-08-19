import pytest

from infracheck.model.DataTypes import DataTypes
from infracheck.model.IModule import IModule


class AddressReachable(IModule):
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

    params = {
        "url": DataTypes.Text
    }

    # noinspection PyMethodParameters
    @pytest.mark.parametrize("data", [params])
    def test(host, data):
        addr = data['url']
        curr_addr = host.addr(addr)
        assert curr_addr.is_resolvable
        assert curr_addr.is_reachable

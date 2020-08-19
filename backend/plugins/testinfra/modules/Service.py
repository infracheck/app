from typing import Dict
from unittest import TestCase

from infracheck.model.DataTypes import DataTypes
from infracheck.model.IModule import IModule
from infracheck.model.IParam import IParam


class Service(IModule, TestCase):
    id = "service"
    version = 0.1
    documentation = """
.. todo:: It should be possible to check for different service states
# Is adress reachable [Linux]
---

## Description:
Check for running services. 

[Testinfra Docs](
https://testinfra.readthedocs.io/en/latest/modules.html#testinfra.modules.service.Service) 
        
## Examples:
```json
# Checking a list of services
{
    "services": ["nginx", "apache2"]
}
```

## Plugin Version
0.1.0

## Author
Martin Welcker <mwelcker@proficom.de>
"""

    params: Dict[str, IParam] = {
        "service": {
            "type": DataTypes.Text,
            "value": ''
        },
        "enabled": {
            "type": DataTypes.Number,
            "value": -1
        },
        "running": {
            "type": DataTypes.Number,
            "value": -1
        }
    }
    host = None

    def test(self):
        service = self.host.service(self.params['service']['value'])
        if self.params['enabled']['value'] == 1:
            assert service.is_enabled
        else:
            assert not service.is_enabled

        if self.params['running']['value'] == 1:
            assert service.is_running
        else:
            assert not service.is_running

from typing import Dict
from unittest import TestCase

import testinfra

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
            "type": DataTypes.Boolean,
            "value": True
        },
        "running": {
            "type": DataTypes.Boolean,
            "value": True
        }
    }
    host = testinfra.get_host("local://")

    def test(self):
        service = self.host.service(self.params['service']['value'])
        should_be_enabled = self.params['enabled']['value']
        should_be_running = self.params['running']['value']

        with self.subTest(F"{service} enabled?"):
            self.assertTrue(
                should_be_enabled == service.is_enabled,
                F"Service {service} is {'enabled' if service.is_enabled else 'disabled'}"
            )
        with self.subTest(F"{service} running?"):
            self.assertTrue(
                should_be_running == service.is_running,
                F"Service {service} is {'running' if service.is_running else 'not running'}"
            )

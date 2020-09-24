from typing import Dict
from unittest import TestCase

import testinfra

from infracheck.model.Types import Types
from infracheck.model.Module import Module
from infracheck.model.Property import Property


class Service(Module, TestCase):
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

    params: Dict[str, Property] = {
        "service": {
            "type": Types.Text,
            "value": ''
        },
        "enabled": {
            "type": Types.Boolean,
            "value": True
        },
        "running": {
            "type": Types.Boolean,
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
import pytest

from infracheck.model.DataTypes import DataTypes
from infracheck.model.ITestModule import ITestModule


class Service(ITestModule):
    id = "service"
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

    fields = {
        "service": DataTypes.Text,
        "enabled": DataTypes.Number,
        "running": DataTypes.Number,
    }

    @pytest.mark.parametrize("data", [fields])
    def test(host, data):
        service = host.service(data['service'])
        if data['enabled'] == 1:
            assert service.is_enabled
        else:
            assert not service.is_enabled

        if data['running'] == 1:
            assert service.is_running
        else:
            assert not service.is_running

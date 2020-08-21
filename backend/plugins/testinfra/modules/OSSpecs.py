from typing import Dict
from unittest import TestCase

from infracheck.model.DataTypes import DataTypes
from infracheck.model.IModule import IModule
from infracheck.model.IParam import IParam


class OSSpecs(IModule, TestCase):
    id = "os_specs"
    version = 0.1
    documentation = """
# Checks specs of operating system [Linux]
---

## Description: 
This test can check for various specs of the operating system. It can be used to check the `type`, 
`distribution`, `release` and `codename` of the hosts os. 

[Testinfra Docs](
https://testinfra.readthedocs.io/en/latest/modules.html#testinfra.modules.systeminfo.SystemInfo) 
        
## Examples:
```json
# Checking a list of hosts
{
    "type": "linux",
    "distribution": "debian",
    "release": "7.8",
    "codename": "wheezy"
}
```

## Plugin Version
0.1.1

## Author
Martin Welcker <mwelcker@proficom.de>
"""
    params: Dict[str, IParam] = {
        "type": {
            "type": DataTypes.Text,
            "value": 'localhost'
        },
        "distribution": {
            "type": DataTypes.Text,
            "value": 'localhost'
        },
        "release": {
            "type": DataTypes.Text,
            "value": 'localhost'
        },
        "codename": {
            "type": DataTypes.Text,
            "value": 'localhost'
        },

    }
    host = None

    def test(self):
        if self.params['type']['value'] != '':
            self.assertTrue(self.host.system_info.type == self.params['type']['value'],
                            F"{self.host.system_info.type} is not {self.params['type']['value']}")
        if self.params['distribution']['value'] != '':
            self.assertTrue(self.host.system_info.distribution == self.params['distribution']['value'],
                            F"{self.host.system_info.distribution} is not {self.params['distribution']['value']}")
        if self.params['release']['value'] != '':
            self.assertTrue(self.host.system_info.release == self.params['release']['value'],
                            F"{self.host.system_info.release} is not {self.params['release']['value']}")
        if self.params['codename']['value'] != '':
            self.assertTrue(self.host.system_info.codename == self.params['codename']['value'],
                            F"{self.host.system_info.codename} is not {self.params['codename']['value']}")

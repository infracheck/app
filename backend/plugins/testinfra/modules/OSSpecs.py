from typing import Dict
from unittest import TestCase

import testinfra

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
    host = testinfra.get_host("local://")

    def test(self):
        os_type = self.params['type']['value']
        distribution = self.params['distribution']['value']
        release = self.params['release']['value']
        codename = self.params['codename']['value']

        with self.subTest("Type"):
            if os_type != '':
                self.assertTrue(
                    self.host.system_info.type == os_type,
                    F"{self.host.system_info.type} != {os_type}"
                )

        with self.subTest("Distribution"):
            if distribution != '':
                self.assertTrue(
                    self.host.system_info.distribution == distribution,
                    F"{self.host.system_info.distribution} != {distribution}"
                )

        with self.subTest("Release"):
            if release != '':
                self.assertTrue(
                    self.host.system_info.release == release,
                    F"{self.host.system_info.release} != {release}"
                )

        with self.subTest("Codename"):
            if codename != '':
                self.assertTrue(
                    self.host.system_info.codename == codename,
                    F"{self.host.system_info.codename} != {codename}"
                )

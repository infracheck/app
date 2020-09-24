from typing import Dict
from unittest import TestCase

import testinfra

from infracheck.model.Types import Types
from infracheck.model.Module import Module
from infracheck.model.Property import Property


class OSSpecs(Module, TestCase):
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
    params: Dict[str, Property] = {
        "type": {
            "type": Types.Text,
            "value": 'localhost'
        },
        "distribution": {
            "type": Types.Text,
            "value": 'localhost'
        },
        "release": {
            "type": Types.Text,
            "value": 'localhost'
        },
        "codename": {
            "type": Types.Text,
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

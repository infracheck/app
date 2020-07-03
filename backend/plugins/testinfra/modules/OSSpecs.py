import pytest

from infracheck.model.DataTypes import DataTypes
from infracheck.model.ITestModule import ITestModule


class OSSpecs(ITestModule):
    id = "os_specs"
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

    fields = {
        "type": DataTypes.Text,
        "distribution": DataTypes.Text,
        "release": DataTypes.Text,
        "codename": DataTypes.Text
    }

    @pytest.mark.parametrize("os_type", [fields["type"]])
    @pytest.mark.parametrize("distribution", [fields["distribution"]])
    @pytest.mark.parametrize("release", [fields["release"]])
    @pytest.mark.parametrize("codename", [fields["codename"]])
    def test(host, os_type, distribution, release, codename):
        if os_type:
            assert host.system_info.type == os_type
        if distribution:
            assert host.system_info.distribution == distribution
        if release:
            assert host.system_info.release == release
        if codename:
            assert host.system_info.codename == codename

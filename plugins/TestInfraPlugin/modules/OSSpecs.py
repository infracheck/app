import pytest

from infracheck.model.DataTypes import DataTypes
from infracheck.model.ITestModule import ITestModule


class OSSpecs(ITestModule):
    name = "os_specs"
    documentation = """
    This test performs a os specification comparison
    """
    fields = {
        "type": DataTypes.Text,
        "distribution": DataTypes.Text,
        "release": DataTypes.Text,
        "codename": DataTypes.Text
    }

    @pytest.mark.parametrize("type", [fields["type"]])
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

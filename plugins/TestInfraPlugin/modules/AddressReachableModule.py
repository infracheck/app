import pytest

from infracheck.model.DataTypes import DataTypes
from infracheck.model.ITestModule import ITestModule


class AddressReachableModule(ITestModule):
    name = "AddressReachableModule"
    version = "1.0"
    documentation = """
    This test performs a regex comparison
    """
    fields = {
        "url": DataTypes.Text
    }

    @pytest.mark.parametrize("fields", [fields])
    def test(host, fields):
        addr = fields['url']
        curr_addr = host.addr(addr)
        assert curr_addr.is_resolvable
        assert curr_addr.is_reachable

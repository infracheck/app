import pytest

from infracheck.model.DataTypes import DataTypes
from infracheck.model.ITestModule import ITestModule


class AddressReachableModule(ITestModule):
    name = "AddressReachableModule"
    documentation = """
    This test performs a regex comparison
    """
    fields = {
        "url": DataTypes.Text
    }

    # noinspection PyMethodParameters
    @pytest.mark.parametrize("data", [fields])
    def test(host, data):
        addr = data['url']
        curr_addr = host.addr(addr)
        assert curr_addr.is_resolvable
        assert curr_addr.is_reachable

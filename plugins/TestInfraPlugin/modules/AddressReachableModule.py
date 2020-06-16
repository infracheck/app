import pytest

from infracheck.model.FieldTypes import DataTypes
from infracheck.model.ITestModule import ITestModule


class AddressReachableModule(ITestModule):
    name = "AddressReachableModule"
    version = "1.0"
    documentation = """
    This test performs a regex comparison
    """
    fields = {
        "url": str(DataTypes.Text.value)
    }

    @pytest.mark.parametrize("addr", [fields["url"]])
    def test(host, addr):
        curr_addr = host.addr(addr)
        assert curr_addr.is_resolvable
        assert curr_addr.is_reachable

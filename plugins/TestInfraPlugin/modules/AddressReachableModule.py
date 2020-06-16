import pytest

from infracheck.model.FieldTypes import FieldType
from infracheck.model.ITestModule import ITestModule


class AddressReachableModule(ITestModule):
    id = "AddressReachableModule"
    version = "1.0"
    documentation = """
    This test performs a regex comparison
    """
    fields = {
        "url": str(FieldType.Text)
    }

    @pytest.mark.parametrize("addr", [fields["url"]])
    def test(host, addr):
        curr_addr = host.addr(addr)
        assert curr_addr.is_resolvable
        assert curr_addr.is_reachable

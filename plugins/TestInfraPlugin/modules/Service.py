import pytest

from infracheck.model.DataTypes import DataTypes
from infracheck.model.ITestModule import ITestModule


class Service(ITestModule):
    name = "service"
    documentation = """
    This test checks running and enabled services
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

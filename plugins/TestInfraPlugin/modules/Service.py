import pytest

from infracheck.model.ITestModule import ITestModule


class Service(ITestModule):
    name = "service"
    documentation = """
    This test checks running and enabled services
    """

    @pytest.mark.parametrize("name,version", [
        ("nginx", "1.6"),
        ("python", "2.7"),
    ])
    def test(host, name, version):
        pkg = host.package(name)
        assert pkg.is_installed
        assert pkg.version.startswith(version)

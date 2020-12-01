import os
from typing import Any

import testinfra


class Connection:
    """
    The connection class is an abstraction of the testinfra host.
    For that it has the property `host`, that can be used for infrastructure tests.
    """
    user: str
    address: str
    password: str
    port: int
    os: str

    def __init__(self, user, host, password, port, os) -> None:
        self.user = user
        self.address = host
        self.password = password
        self.port = port
        self.os = os
        self.name = F'{os}_{user}@{host}:{port}'

    @property
    def host(self) -> Any:
        """
        This property is the actual testinfra host to run tests on.
        It is implemented as a factory method, that returns the testinfra host object.
        :return:
        """
        if self.address in ['localhost', '127.0.0.1']:
            return self._get_localhost()
        elif self.os == 'linux':
            return self._get_linux_host()
        elif self.os == 'windows':
            return self._get_windows_host()
        else:
            raise AttributeError("'os' must be either 'linux' or 'windows'")

    @staticmethod
    def _get_localhost():
        return testinfra.get_host("local://")

    def _get_windows_host(self):
        return testinfra.get_host(
            F"winrm://{self.user}:{self.password}@{self.address}:{self.port}?no_ssl=true&no_verify_ssl=true")

    def _get_linux_host(self):
        return testinfra.get_host(
            F"ssh://{self.user}:{self.password}@{self.address}:{self.port}?"
            F"ssh_config={os.path.dirname(__file__)}/ssh-config&no_ssl=true&no_verify_ssl=true&o=true")

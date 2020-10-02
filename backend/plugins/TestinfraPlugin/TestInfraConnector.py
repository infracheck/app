from typing import Any

import testinfra

from plugins.TestinfraPlugin.Configuration import Configuration


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
            host = self._get_localhost()
        elif self.os == 'linux':
            host = self._get_linux_host()
        elif self.os == 'windows':
            host = self._get_windows_host()
        return host

    def _get_localhost(self):
        return testinfra.get_host("local://")

    def _get_windows_host(self):
        return testinfra.get_host(
            F"winrm://{self.user}:{self.password}@{self.address}:{self.port}?no_ssl=true&no_verify_ssl=true")

    def _get_linux_host(self):
        return testinfra.get_host(
            F"paramiko://{self.user}@{self.address}:{self.port}?ssh_identity_file={Configuration.SSH_FOLDER}id_rsa&no_ssl=true&no_verify_ssl=true")

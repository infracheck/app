from dataclasses import dataclass
from typing import Any

import testinfra

from plugins.TestinfraPlugin.Configuration import Configuration


@dataclass
class Connection:
    user: str
    host: str
    password: str
    port: int
    os: str

    def get_host(self) -> Any:
        if self.host == 'localhost':
            return self._get_localhost()
        elif self.os == 'linux':
            return self._get_linux_host()
        elif self.os == 'windows':
            return self._get_windows_host()
        else:
            raise ValueError

    def _get_localhost(self):
        print("LOCAL HOST")
        return testinfra.get_host("local://")

    def _get_windows_host(self):
        print("WINDOWS HOST")
        return testinfra.get_host(
            F"winrm://{self.user}:{self.password}@{self.host}:{self.port}?no_ssl=true&no_verify_ssl=true")

    def _get_linux_host(self):
        return testinfra.get_host(
            F"paramiko://{self.user}@{self.host}:{self.port}?ssh_identity_file={Configuration.SSH_FOLDER}id_rsa&no_ssl=true&no_verify_ssl=true")

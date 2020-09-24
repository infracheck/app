from abc import ABC, abstractmethod
from dataclasses import dataclass

import testinfra

from plugins.TestinfraPlugin.Configuration import Configuration


@dataclass
class Connection:
    user: str
    host: str
    password: str
    port: int


class TestInfraConnector(ABC):
    def __init__(self, conn: Connection) -> None:
        self.username = conn.user
        self.host = conn.host
        self.password = conn.password
        self.port = conn.port

    @abstractmethod
    def get_host(self):
        raise NotImplementedError


class LocalhostConnector(TestInfraConnector):

    def __init__(self, conn: Connection) -> None:
        super().__init__(conn)

    def get_host(self):
        return testinfra.get_host("local://")


class WinRmConnector(TestInfraConnector):

    def __init__(self, conn: Connection) -> None:
        super().__init__(conn)

    def get_host(self):
        return testinfra.get_host(
            F"winrm://{self.username}:{self.password}@{self.host}:{self.port}?no_ssl=true&no_verify_ssl=true")


class ParamikoConnector(TestInfraConnector):
    def __init__(self, conn: Connection) -> None:
        super().__init__(conn)

    def get_host(self):
        return testinfra.get_host(
            F"paramiko://{self.username}@{self.host}:{self.port}?ssh_identity_file={Configuration.SSH_FOLDER}id_rsa&no_ssl=true&no_verify_ssl=true")

from abc import ABC, abstractmethod

import testinfra

from plugins.testinfra.Config import Config


class TestInfraConnector(ABC):
    def __init__(self, username='user', host='localhost', password='password', port=22) -> None:
        self.username = username
        self.host = host
        self.password = password
        self.port = port

    @abstractmethod
    def get_host(self):
        raise NotImplementedError


class LocalhostConnector(TestInfraConnector):

    def __init__(self) -> None:
        super().__init__()

    def get_host(self):
        return testinfra.get_host("local://")


class WinRmConnector(TestInfraConnector):

    def __init__(self, username, host, password, port) -> None:
        super().__init__(username, host, password, port)
        self.username = username
        self.host = host
        self.password = password
        self.port = port

    def get_host(self):
        return testinfra.get_host(
            F"winrm://{self.username}:{self.password}@{self.host}:{self.port}?no_ssl=true&no_verify_ssl=true")


class ParamikoConnector(TestInfraConnector):
    def __init__(self, username, host, password, port) -> None:
        super().__init__(username, host, password, port)
        self.username = username
        self.host = host
        self.password = password
        self.port = port

    def get_host(self):
        return testinfra.get_host(
            F"paramiko://{self.username}@{self.host}:{self.port}?ssh_identity_file={Config.SSH_FOLDER}id_rsa&no_ssl=true&no_verify_ssl=true")

from dataclasses import dataclass

from infracheck.Plugin import Plugin
from infracheck.model.Types import Types
from plugins.TestinfraPlugin.KeyRegistration import KeyRegistration
from plugins.TestinfraPlugin.TestInfraConnector import Connection


class TestInfraPlugin(Plugin):
    """
    """
    __version__ = 0.5

    @dataclass
    class props:
        host_address: Types.Text = "localhost"
        username: Types.Text = ""
        os: Types.Text = "linux"
        password: Types.Password = ""
        port: Types.Number = 22

    ssh_service: KeyRegistration

    def setup(self):
        self.props.host = Connection(
            password=self.props.password,
            host=self.props.host_address,
            user=self.props.username,
            port=self.props.port,
            os=self.props.os,
        ).get_host()

        if self.props.os == 'linux':
            self.ssh_service = KeyRegistration(
                user=self.props.username,
                password=self.props.password,
                port=self.props.port
            )
            self.ssh_service.register_ssh_keys([self.props.host_address])

    def tear_down(self):
        if self.props.os == 'linux':
            self.ssh_service.clean_ssh_keys([self.props.host_address])

from dataclasses import dataclass

from infracheck.Plugin import Plugin
from infracheck.model.Types import Types
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

    def setup(self):
        self.props.host = Connection(
            password=self.props.password,
            host=self.props.host_address,
            user=self.props.username,
            port=self.props.port,
            os=self.props.os,
        ).get_host()

    def tear_down(self):
        print("no before action")

from dataclasses import dataclass
from unittest import TestCase

from infracheck.Module import Module
from infracheck.model.Types import Types


class Service(Module, TestCase):
    """
    # Check for running services
    ---

    ## Description:
    Check for running services.

    [Testinfra Docs](
    https://testinfra.readthedocs.io/en/latest/modules.html#testinfra.modules.service.Service)

    ## Author
    Martin Welcker <mwelcker@proficom.de>
    """
    __version__ = 0.1

    @dataclass
    class props:
        service: Types.Text = ""
        enabled: Types.Boolean = True
        running: Types.Boolean = True

    def test(self):
        service = self.plugin_props.host.service(self.props.service)
        should_be_enabled = self.props.enabled
        should_be_running = self.props.running

        with self.subTest(F"{service} enabled?"):
            self.assertTrue(
                should_be_enabled == service.is_enabled,
                F"Service {service} is {'enabled' if service.is_enabled else 'disabled'}"
            )
        with self.subTest(F"{service} running?"):
            self.assertTrue(
                should_be_running == service.is_running,
                F"Service {service} is {'running' if service.is_running else 'not running'}"
            )

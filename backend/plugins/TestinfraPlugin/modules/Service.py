from dataclasses import dataclass

from infracheck.Module import Module
from infracheck.model.TestResult import ModuleResult
from infracheck.model.Types import Types


class Service(Module):
    """Check for running services.

    [Testinfra Docs](
    https://testinfra.readthedocs.io/en/latest/modules.html#testinfra.modules.service.Service)
    """
    __version__ = 0.1

    @dataclass
    class props:
        service: Types.Text = ""
        enabled: Types.Boolean = True
        running: Types.Boolean = True

    def test(self) -> ModuleResult:
        service = self.plugin_props.host.service(self.props.service)

        equal_enabled = self.props.enabled == service.is_enabled
        equal_running = self.props.running == service.is_running

        return ModuleResult(
            result_successful=equal_enabled and equal_running,
            result_message=
            "Service works as expected"
            if equal_running and equal_enabled else
            "Service not as expected",
            result_data={
                "service_is_enabled": service.is_enabled,
                "service_is_running": service.is_running
            },
        )

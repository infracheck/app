from infracheck.Module import Module
from infracheck.model.TestResult import ModuleResult
from infracheck.model.Types import Types


class CheckServiceSpecs(Module):
    """
Check if services are running or enabled.

[Testinfra Docs](https://testinfra.readthedocs.io/en/latest/modules.html#testinfra.modules.service.Service)

## Properties
* `service`: Name of the service to check (e.g.: `docker`, `nginx`, `apache2`)
* `enabled`: Check if the service is enabled or not
* `running`: Check if the service is running or not running.

## To do
* `is_valid`: Test if service is valid. This method is only available in the systemd implementation, it will raise NotImplementedError in others implementation
* `is_masked`: Test if service is masked. This method is only available in the systemd implementation, it will raise NotImplementedError in others implementations
    """
    __version__ = 0.1
    __author__ = "Martin Welcker <mwelcker@proficom.de>"
    __compatibility__ = "Linux"

    class props:
        service: Types.Text = "docker"
        enabled: Types.Boolean = True
        running: Types.Boolean = True

    def test(self) -> ModuleResult:
        result_successful = True
        result_message = ""
        result_data = {}

        for connection in self.plugin_props.connections:
            host = connection.host
            service = host.service(self.props.service)
            equal_enabled = self.props.enabled == service.is_enabled
            equal_running = self.props.running == service.is_running

            if not equal_running or not equal_enabled:
                result_successful = False
                result_message += F"{connection.name}: " \
                                  F"{'Service works as expected' if equal_running and equal_enabled else 'Service not as expected'}"

            result_data[connection.name] = {
                "is_enabled": service.is_enabled,
                "is_running": service.is_running
            }

        return ModuleResult(result_successful, result_message, result_data)

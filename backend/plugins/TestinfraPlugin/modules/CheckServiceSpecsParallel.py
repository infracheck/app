from multiprocessing import Pool

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

    def _test(self, host):
        service = host.service(self.props.service)
        return {
            "equal_enabled": self.props.enabled == service.is_enabled,
            "equal_running": self.props.running == service.is_running
        }

    def test(self) -> ModuleResult:
        result_successful = True
        result_message = ""
        result_data = {}

        with Pool(processes=10) as pool:
            multiple_results = [pool.apply_async(self._test, (host,)) for host in self.plugin_props.connections]
            results = ([res.get() for res in multiple_results])

            for result in results:
                if not result["equal_running"] or not result["equal_enabled"]:
                    result_successful = False
                    result_message += F"TODO: " \
                                      F"{'Service works as expected' if result['equal_running'] and result['equal_enabled'] else 'Service not as expected'}"

                result_data = {}

        return ModuleResult(result_successful, result_message, result_data)

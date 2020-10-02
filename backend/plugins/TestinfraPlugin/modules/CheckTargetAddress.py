from infracheck.Module import Module
from infracheck.model.TestResult import ModuleResult
from infracheck.model.Types import Types


class CheckTargetReachable(Module):
    """
This module can be used to test ip addresses or host names.
It can check whether they are resolvable or reachable by the host.
[Testinfra Docs](https://testinfra.readthedocs.io/en/latest/modules.html#testinfra.modules.addr.Addr)

## Properties
* `url`: IP addresses to test
* `resolvable`: Checks if address is resolvable
* `reachable`: Checks if address is reachable

## To do
Implement the following `testinfra` `address` features:
* `ip_addresses`: Return IP addresses of host
* `ipv4_addresses`: Return IPv4 addresses of host
* `ipv6_addresses`: Return IPv6 addresses of host
* `port`: Return address-port pair
"""
    __version__ = 1.0
    __author__ = "Martin Welcker <mwelcker@proficom.de>"
    __compatibility__ = "Linux"

    class props:
        url: Types.Text = "google.de"
        reachable: Types.Boolean = True
        resolvable: Types.Boolean = True

    def test(self) -> ModuleResult:
        result_data = {}
        result_message = ''
        result_successful = True

        for connection in self.plugin_props.connections:
            host = connection.host
            is_resolvable = host.addr(self.props.url).is_resolvable
            is_reachable = host.addr(self.props.url).is_reachable

            if is_resolvable != self.props.resolvable or is_reachable != self.props.reachable:
                result_successful = False
                result_message += F"Failed for '{connection.name}' | "

            result_data[connection.name] = {
                "address_is_resolvable": is_resolvable,
                "address_is_reachable": is_reachable
            }

        return ModuleResult(result_successful, result_message, result_data)

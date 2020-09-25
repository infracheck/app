from dataclasses import dataclass

from infracheck.Module import Module
from infracheck.model.TestResult import ModuleResult
from infracheck.model.Types import Types


class AddressReachable(Module):
    """
    # Is address reachable [Linux]
    ---

    ## Description:
    This test checks if a list of hosts is reachable.

    [Testinfra Docs](
    https://testinfra.readthedocs.io/en/latest/modules.html#testinfra.modules.addr.Addr)

    ## Examples:
    ```json
    # Checking a list of hosts
    {"addr_list": ["google.de", "proficom.de"]}

    # Checking for a single hosts
    {"addr_list": ["google.de"]}

    # Checks for
    {"addr_list": ["192.168.0.10", "127.0.0.1"]}
    ```

    ## Plugin Version
    0.1.1


    ## Author
    Martin Welcker <mwelcker@proficom.de>
    """

    __version__ = 0.1

    @dataclass
    class props:
        url: Types.Text = "google.de"

    def test(self) -> ModuleResult:
        is_resolvable = self.plugin_props.host.addr(self.props.url).is_resolvable
        is_reachable = self.plugin_props.host.addr(self.props.url).is_reachable

        return ModuleResult(
            result_successful=is_reachable and is_reachable,
            result_data={
                "resolvable": is_resolvable,
                "is_reachable": is_reachable
            },
            result_message=F"Address is {'resolvable' if is_resolvable else 'not resolvable'}. "
                           F"Address is {'reachable' if is_reachable else 'not reachable'}."
        )

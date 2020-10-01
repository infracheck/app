from dataclasses import dataclass

from infracheck.Module import Module
from infracheck.model.TestResult import ModuleResult
from infracheck.model.Types import Types


class AddressReachable(Module):
    """
    This test checks if a list of hosts is reachable.
    [Testinfra Docs](
    https://testinfra.readthedocs.io/en/latest/modules.html#testinfra.modules.addr.Addr)
    """

    __version__ = 0.1

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

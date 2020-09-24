from dataclasses import dataclass
from unittest import TestCase

import testinfra

from infracheck.Module import Module
from infracheck.model.TestResult import ModuleResult
from infracheck.model.Types import Types


class AddressReachable(Module, TestCase):
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
        addr = self.props.url

        with self.subTest("Resolvable"):
            self.assertTrue(
                self.plugin_props.host.addr(addr).is_resolvable,
                F"Address {addr} is not resolvable"
            )

        with self.subTest("Reachable"):
            self.assertTrue(
                self.plugin_props.host.addr(addr).is_reachable,
                F"Address {addr} is not resolvable"
            )
        return ModuleResult()

from dataclasses import dataclass
from unittest import TestCase

import testinfra

from infracheck.Module import Module
from infracheck.model.TestResult import ModuleResult
from infracheck.model.Types import Types


class OSSpecs(Module, TestCase):
    """
    # Checks specs of operating system [Linux]
    ---
    ## Description:
    This test can check for various specs of the operating system. It can be used to check the `type`,
    `distribution`, `release` and `codename` of the hosts os.

    [Testinfra Docs](
    https://testinfra.readthedocs.io/en/latest/modules.html#testinfra.modules.systeminfo.SystemInfo)

    ## Author
    Martin Welcker <mwelcker@proficom.de>
    """
    __version__ = 0.1

    @dataclass
    class props:
        type: Types.Text = ""
        distribution: Types.Text = ""
        release: Types.Text = ""
        codename: Types.Text = ""


    def test(self) -> ModuleResult:
        os_type = self.props.type
        distribution = self.props.distribution
        release = self.props.release
        codename = self.props.codename

        with self.subTest("Type"):
            if os_type != '':
                self.assertTrue(
                    self.plugin_props.host.system_info.type == os_type,
                    F"{self.plugin_props.host.system_info.type} != {os_type}"
                )

        with self.subTest("Distribution"):
            if distribution != '':
                self.assertTrue(
                    self.plugin_props.host.system_info.distribution == distribution,
                    F"{self.plugin_props.host.system_info.distribution} != {distribution}"
                )

        with self.subTest("Release"):
            if release != '':
                self.assertTrue(
                    self.plugin_props.host.system_info.release == release,
                    F"{self.plugin_props.host.system_info.release} != {release}"
                )

        with self.subTest("Codename"):
            if codename != '':
                self.assertTrue(
                    self.plugin_props.host.system_info.codename == codename,
                    F"{self.plugin_props.host.system_info.codename} != {codename}"
                )

        return ModuleResult()

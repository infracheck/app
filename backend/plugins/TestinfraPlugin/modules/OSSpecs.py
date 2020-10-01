from dataclasses import dataclass

from infracheck.Module import Module
from infracheck.model.TestResult import ModuleResult
from infracheck.model.Types import Types


class OSSpecs(Module):
    """This test can check for various specs of the operating system. It can be used to check the `type`,
    `distribution`, `release` and `codename` of the hosts os.

    [Testinfra Docs](
    https://testinfra.readthedocs.io/en/latest/modules.html#testinfra.modules.systeminfo.SystemInfo)
    """
    __version__ = 0.1

    class props:
        type: Types.Text = ""
        distribution: Types.Text = ""
        release: Types.Text = ""
        codename: Types.Text = ""

    def test(self) -> ModuleResult:
        host = self.plugin_props.host

        result = {}
        is_successful = True
        if self.props.type != "":
            equal_type = host.system_info.type == self.props.type
            result["equal_type"] = F"'{host.system_info.type}'" \
                                   F"{'==' if equal_type else '!='}" \
                                   F"'{self.props.type}'"
            is_successful = equal_type

        if self.props.distribution != "":
            equal_distribution = host.system_info.distribution == self.props.distribution
            result["equal_distribution"] = F"'{host.system_info.distribution}'" \
                                           F"{'==' if equal_distribution else '!='}" \
                                           F"'{self.props.distribution}'"
            is_successful = equal_distribution

        if self.props.release != "":
            equal_release = host.system_info.release == self.props.release
            result["equal_release"] = F"'{host.system_info.release}'" \
                                      F"{'==' if equal_release else '!='}" \
                                      F"'{self.props.release}'"
            is_successful = equal_release

        if self.props.codename != "":
            equal_codename = host.system_info.codename == self.props.codename
            result["equal_codename"] = F"'{host.system_info.codename}'" \
                                       F"{'==' if equal_codename else '!='}" \
                                       F"'{self.props.codename}'"
            is_successful = equal_codename

        return ModuleResult(
            result_successful=is_successful,
            result_message="System information are correct" if is_successful else "System information are incorrect",
            result_data=result
        )

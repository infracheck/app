from infracheck.Module import Module
from infracheck.model.TestResult import ModuleResult
from infracheck.model.Types import Types


class CheckOperatingSystemSpecs(Module):
    """
    This test can check for various specs of the operating system.
    It can be used to check the `type`, `distribution`, `release` and `codename` of the hosts os.

    [Testinfra Docs](https://testinfra.readthedocs.io/en/latest/modules.html#testinfra.modules.systeminfo.SystemInfo)

    ## Properties
    * `type`: Check OS type (e.g.: `linux`, `windows`)
    * `distribution`: Check distribution name (e.g.: `debian`, `fedora`)
    * `release`: Check distribution release number (e.g.: `10.2`, `44.1`)
    * `codename`: Check release code name (e.g.: `buster`, `Heisenbug`)

    ## To do
    * `arch`: Checks host architecture (`x86_64`, `arm`)
    """
    __version__ = 0.1
    __author__ = "Martin Welcker <mwelcker@proficom.de>"
    __compatibility__ = "Linux"

    class props:
        type: Types.Text = ""
        distribution: Types.Text = ""
        release: Types.Text = ""
        codename: Types.Text = ""

    def test(self) -> ModuleResult:
        result = {}
        is_successful = True

        for connection in self.plugin_props.connections:
            host = connection.host
            print(host)
            result[connection.name] = {}
            if self.props.type != "":
                equal_type = host.system_info.type == self.props.type
                result[connection.name]["equal_type"] = F"'{host.system_info.type}'" \
                                                        F"{'==' if equal_type else '!='}" \
                                                        F"'{self.props.type}'"
                is_successful = equal_type

            if self.props.distribution != "":
                equal_distribution = host.system_info.distribution == self.props.distribution
                result[connection.name]["equal_distribution"] = F"'{host.system_info.distribution}'" \
                                                                F"{'==' if equal_distribution else '!='}" \
                                                                F"'{self.props.distribution}'"
                is_successful = equal_distribution

            if self.props.release != "":
                equal_release = host.system_info.release == self.props.release
                result[connection.name]["equal_release"] = F"'{host.system_info.release}'" \
                                                           F"{'==' if equal_release else '!='}" \
                                                           F"'{self.props.release}'"
                is_successful = equal_release

            if self.props.codename != "":
                equal_codename = host.system_info.codename == self.props.codename
                result[connection.name]["equal_codename"] = F"'{host.system_info.codename}'" \
                                                            F"{'==' if equal_codename else '!='}" \
                                                            F"'{self.props.codename}'"
                is_successful = equal_codename

        message = "System information are correct" if is_successful else "System information are incorrect"
        return ModuleResult(is_successful, message, result)

import os
import subprocess

from infracheck.model.IPlugin import PluginData, TestResult, IPlugin


class TestInfraPlugin(IPlugin):
    package_name = F"{os.path.basename(__file__).split('.')[0]}"
    id = 'TestInfraPlugin'
    version = '0.1'
    documentation = """
    This Testinfra plugins enable you to run customized code snippets using the testinfra framework
    """

    def __init__(self):
        super().__init__()
        self.reload_modules()

    def test(self, data: PluginData) -> TestResult:
        # Create Testfile

        # Run Testfile
        subprocess.call("py.test -v example-testinfra.py", shell=True)
        return data

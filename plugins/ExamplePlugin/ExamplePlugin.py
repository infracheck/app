import os

from infracheck.model.IPlugin import PluginData, TestResult, IPlugin


class ExamplePlugin(IPlugin):
    package_name = F"{os.path.basename(__file__).split('.')[0]}"
    id = 'ExamplePlugin'
    version = '0.1'
    documentation = """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut 
    labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip 
    ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat 
    nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id 
    est laborum. """

    def __init__(self):
        super().__init__()
        self.reload_modules()

    def test(self, data: PluginData) -> TestResult:
        return {
            'succeededd': 23121,
            'failed': 2
        }

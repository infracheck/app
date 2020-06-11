import os

from infracheck.model.IPlugin import PluginData, TestResult, IPlugin


class Example(IPlugin):
    def __init__(self):
        super().__init__()
        self.id = 'example'
        self.version = '1.0'
        self.documentation = '1.0'
        self.package_name = F"plugins.{os.path.basename(__file__).split('.')[0]}.modules"
        self.reload_modules(self.package_name)

    def test(self, data: PluginData) -> TestResult:
        return {
            'succeededd': 1,
            'failed': 2
        }

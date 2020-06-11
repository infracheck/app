import os

from infracheck.model.IPlugin import PluginData, TestResult, IPlugin


class Example(IPlugin):
    def __init__(self):
        super().__init__()
        self.id = 'example'
        self.version = '1.0'
        self.package_name = F"plugins.{os.path.basename(__file__).split('.')[0]}.modules"
        self.reload_modules(self.package_name)

    def test(self, data: PluginData) -> TestResult:
        failed = 0
        succeeded = 0
        for number in data['numbers']:
            print(number % 2)
            if number % 2 == 0:
                succeeded += 1
            else:
                failed += 1

        return {
            'succeededd': succeeded,
            'failed': failed
        }

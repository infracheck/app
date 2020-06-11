import os

from infracheck.model.IPlugin import PluginData, TestResult, IPlugin


class Example(IPlugin):
    package_name = F"{os.path.basename(__file__).split('.')[0]}"
    id = 'exadasdas dasd asddample'
    version = '1.1'
    documentation = '1.0'

    def __init__(self):
        super().__init__()
        self.reload_modules()

    def test(self, data: PluginData) -> TestResult:
        return {
            'succeededd': 23121,
            'failed': 2
        }

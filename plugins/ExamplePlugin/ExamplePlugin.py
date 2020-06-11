from infracheck.IPlugin import TestResult, IPlugin, PluginData


class Example(IPlugin):
    def __init__(self):
        super().__init__()
        self.id = 'example'
        self.version = '1.0'

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

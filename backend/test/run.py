import unittest

from Environment import Environment

if __name__ == '__main__':
    Environment.LOG_LEVEL = 'WARNING'
    loader = unittest.TestLoader()
    start_dir = '.'
    suite = loader.discover('')

    runner = unittest.TextTestRunner(verbosity=0)
    runner.run(suite)

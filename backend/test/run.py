import unittest


if __name__ == '__main__':
    loader = unittest.TestLoader()
    start_dir = '.'
    suite = loader.discover('')

    runner = unittest.TextTestRunner(verbosity=0)
    runner.run(suite)

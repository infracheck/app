import unittest

from infracheck import app


class TestrunTest(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_testrun(self):
        pass

    def test_failing_testrun(self):
        pass

    def tearDown(self) -> None:
        yield self.client

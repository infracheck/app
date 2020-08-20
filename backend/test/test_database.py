import os
import unittest

from infracheck import Persistence
from test import mock_data


class DatabaseTest(unittest.TestCase):
    def setUp(self):
        self.db = Persistence()

    def test_log_table(self):
        with self.subTest("database was created"):
            self.assertTrue(os.path.isfile('infracheck.db'))

        with self.subTest("'Logs' table exists"):
            self.assertTrue(self.db.get_log() == [])

        with self.subTest("New result was added"):
            self.db.insert_test_result(mock_data.result_mock)
            self.assertTrue(len(self.db.get_log()) > 0)

    def tearDown(self) -> None:
        os.remove(F'infracheck.db')

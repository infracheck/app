import unittest
from typing import List

from infracheck import app


class ApiTest(unittest.TestCase):
    def setUp(self) -> None:
        self.client = app.test_client()

    def test_swagger(self):
        response = self.client.get('/swagger.json')
        with self.subTest("'/swagger.json' exists"):
            self.assertTrue(response.status_code == 200)
        with self.subTest("data contains swagger json"):
            self.assertTrue('swagger' in response.json())

    def test_plugins(self):
        response = self.client.get('/plugins')
        with self.subTest("'/plugins' exists"):
            self.assertTrue(response.status_code == 200)
        with self.subTest("data is of type list"):
            self.assertTrue(isinstance(response.json(), List))

    def tearDown(self) -> None:
        yield self.client

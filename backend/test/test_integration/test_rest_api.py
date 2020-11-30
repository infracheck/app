import unittest

from jsonschema import validate

from infracheck import app
from infracheck.model.schemes import plugin_scheme


class RestAPITest(unittest.TestCase):
    """
    S-1 - REST-API
    I-3 - Datenformate
    """
    def setUp(self) -> None:
        self.client = app.test_client()
        app.config['SECURE_API'] = False

    def test_swagger(self):
        response = self.client.get('/swagger.json')
        with self.subTest("'/swagger.json' exists"):
            self.assertTrue(response.status_code == 200)
        with self.subTest("data contains swagger json"):
            self.assertTrue('swagger' in response.get_json())
        with self.subTest("is version 2.0"):
            self.assertTrue('2.0' == response.get_json()['swagger'])

    def test_plugins(self):
        response = self.client.get('/plugins')
        with self.subTest("'/plugins' exists"):
            self.assertTrue(response.status_code == 200)
        with self.subTest("data is of type list"):
            self.assertIsNone(validate(response.get_json(), plugin_scheme))

    def tearDown(self) -> None:
        yield self.client

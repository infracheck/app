import os
import unittest

from infracheck import app

test_data = {
    "name": "Just another test",
    "description": "Hey there its me",
    "plugins": [
        {
            "id": "demo_plugin",
            "params": {},
            "modules": [
                {
                    "id": "equality_check",
                    "params": {
                        "number1": 1,
                        "number2": 1
                    }
                }
            ]
        }
    ]
}


class TestrunTest(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_testrun(self):
        test_data['plugins'][0]['modules'][0]['params'] = {
            "number1": 1,
            "number2": 1}
        response = self.client.post('/test', json=test_data)
        with self.subTest("'/test' exists"):
            self.assertTrue(response.status_code == 200)
        with self.subTest("test succeeded"):
            self.assertTrue(response.get_json()['success_count'] == 1)

    def test_failing_testrun(self):
        test_data['plugins'][0]['modules'][0]['params'] = {
            "number1": -1,
            "number2": 1}
        response = self.client.post('/test', json=test_data)
        with self.subTest("'/test' exists"):
            self.assertTrue(response.status_code == 200)
        with self.subTest("test failed"):
            self.assertTrue(response.get_json()['success_count'] == 0)

    def tearDown(self) -> None:
        os.remove(F'infracheck.db')
        yield self.client

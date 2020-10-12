import unittest

from infracheck import app
from test import mock_data


class ApiTest(unittest.TestCase):
    USERNAME = "user"
    PASSWORD = "pw"
    token = ''

    def setUp(self) -> None:
        self.client = app.test_client()
        app.config['SECURE_API'] = True
        app.config['PASSWORD'] = self.PASSWORD

    def test_failing_authentication(self):
        response = self.client.post('/login', json={"username": "WRONG_USER", "password": "WRONG_PW"})
        with self.subTest("access denied"):
            self.assertTrue(response.status_code == 401)

        with self.subTest("Access denied on /plugins"):
            self.assertEqual(self.client.get('/plugins').status_code, 401)

    def test_authentication(self):
        response = self.client.post('/login', json={"username": self.USERNAME, "password": self.PASSWORD})
        data = response.get_json()

        with self.subTest("status code 200"):
            self.assertTrue(response.status_code == 200)

        with self.subTest("data contains JWT key"):
            self.assertTrue('access_token' in data)
            token = data['access_token']

        header = {
            'Authorization': F'Bearer {token}'
        }

        with self.subTest("on /plugins"):
            self.assertTrue(self.client.get('/plugins', headers=header).status_code == 200)

        with self.subTest("on /results"):
            self.assertTrue(self.client.get('/results', headers=header).status_code == 200)

        with self.subTest("on /test"):
            self.assertTrue(
                self.client.post(
                    '/test',
                    json=mock_data.localhost_test_data,
                    headers=header).status_code == 200)

        with self.subTest("successful /logout"):
            response = self.client.post('/logout', headers=header)
            self.assertTrue(response.status_code == 200)

    def tearDown(self) -> None:
        yield self.client

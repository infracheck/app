import os
import unittest

from infracheck import app
from test import mock_data


class TestrunTest(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config['BASIC_AUTH_FORCE'] = False

    def test_run(self):
        response = self.client.post('/test', json=mock_data.localhost_test_data)
        json = response.get_json()

        with self.subTest("status code == 200"):
            self.assertTrue(response.status_code == 200)

        with self.subTest("returns json"):
            self.assertEqual(response.headers.get('Content-Type'), "application/json")

        id = json['id']
        with self.subTest(F"has an id"):
            self.assertIsNotNone(json['id'])

        with self.subTest(F"generated a pdf document"):
            response = self.client.get(F"/results/{id}.pdf")
            self.assertTrue(response.status_code == 200)
            self.assertEqual(response.headers.get('Content-Type'), "application/pdf")

        # Remove that pdf
        pdf = F"{app.config['RESULT_FOLDER']}/{id}.pdf"
        if os.path.isfile(pdf):
            os.remove(pdf)

    def tearDown(self) -> None:
        yield self.client

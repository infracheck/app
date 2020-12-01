import unittest

from infracheck import app
from test import mock_data


class TestExecutionTest(unittest.TestCase):
    """
    K-1 - Ausführung von Infrastrukturtests
    K-2 - Abruf der Testresultaten
    """

    def setUp(self):
        self.client = app.test_client()
        app.config['SECURE_API'] = False

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
            response = self.client.get(F"/results/pdf/{id}.pdf")
            self.assertTrue(response.status_code == 200)
            self.assertEqual(response.headers.get('Content-Type'), "application/pdf")

        with self.subTest("retrieve result after test"):
            response = self.client.get(F"/results/{id}")
            self.assertTrue(response.status_code == 200)
            self.assertEqual(response.headers.get('Content-Type'), "application/json")

    def tearDown(self) -> None:
        yield self.client

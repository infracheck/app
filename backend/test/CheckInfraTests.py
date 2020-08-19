import inspect
import os
import unittest

from infracheck import Persistence, app
from infracheck.PluginManager import PluginManager
from test.data import result


class ApiTest(unittest.TestCase):
    def setUp(self) -> None:
        self.client = app.test_client()

    def test_swagger(self):
        response = self.client.get('/swagger.json')
        with self.subTest("'/swagger.json' exists"):
            self.assertTrue(response.status_code == 200)
        with self.subTest("data contains swagger json"):
            self.assertTrue('swagger' in response.get_json())

    def tearDown(self) -> None:
        del self.client


class DatabaseTest(unittest.TestCase):
    def setUp(self):
        self.db = Persistence()

    def test_log_table(self):
        with self.subTest("database was created"):
            self.assertTrue(os.path.isfile('infracheck.db'))

        with self.subTest("'Logs' table exists"):
            self.assertTrue(self.db.get_log() == [])

        with self.subTest("New result was added"):
            self.db.insert_test_result(result)
            self.assertTrue(len(self.db.get_log()) > 0)

    def tearDown(self) -> None:
        os.remove('infracheck.db')


class PluginsTest(unittest.TestCase):
    def setUp(self):
        self.plugin_manager = PluginManager()

    def test_plugins(self):
        with self.subTest("'testinfra' exists"):
            self.assertTrue(any(x.id == "testinfra" for x in self.plugin_manager.plugins))

        with self.subTest("'demo_plugin' exists"):
            self.assertTrue(any(x.id == "demo_plugin" for x in self.plugin_manager.plugins))

        for plugin in self.plugin_manager.plugins:
            with self.subTest(F"test() is implemented in {plugin.id}"):
                methods = inspect.getmembers(plugin, inspect.ismethod)
                self.assertTrue(any(x[0] == "test" for x in methods))


def suite():
    suite = unittest.TestSuite()
    suite.addTest(ApiTest())
    suite.addTest(PluginsTest())
    suite.addTest(DatabaseTest())
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())

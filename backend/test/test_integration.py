import unittest
import uuid
from datetime import datetime

import docker
from jsonschema import validate

from infracheck import app
from infracheck.Api import convert_test_input_json_to_dataclasses
from infracheck.PluginManager import PluginManager
from infracheck.model.TestResult import TestResult
from infracheck.model.schemes import plugin_scheme
from infracheck.services.Persistence import Persistence
from test import mock_data


def check_docker_daemon() -> bool:
    try:
        docker.from_env().info()
    except:
        return False
    return True


class DemoPluginTest(unittest.TestCase):
    """
    E-5 - Demo-Plugin
    """

    def test_valid_demo_plugin_format(self):
        plugin_id = "DemoPlugin"
        module_id = "DemoModule"
        with self.subTest(F"'{plugin_id}' exists"):
            plugin = PluginManager()._get_plugin_instance(plugin_id)
            self.assertTrue(plugin.__id__ == plugin_id, F"'{plugin_id}' exists")

        with self.subTest(F"'{plugin_id}' has just one module"):
            self.assertEqual(len(plugin._modules), 1)

        with self.subTest(F"'{plugin_id}' has a '{module_id}' module"):
            module = plugin._get_module_instance(module_id)
            self.assertTrue(module.__id__ == module_id, F"'{module_id}' exists")


class FunctionalPluginTest(unittest.TestCase):
    """
    E-4 - Integration eines Plugins
    P-1 - Integration von ssh- und winrm-Schnittstellen
    Sk-1 - Testen mehrerer Hosts
    I-5 - Entfernen empfindlicher Informationen
    """
    DOCKER_IMAGE_NAME = 'ubuntu-sshd'
    TEST_HOST_COUNT = 3

    @classmethod
    @unittest.skipUnless(check_docker_daemon(), "Skip during pipeline")
    def setUpClass(cls) -> None:
        plugin_id = "TestInfraPlugin"
        cls.plugin_manager = PluginManager()
        cls.plugin = cls.plugin_manager._get_plugin_instance(plugin_id)

        # Setup two containers for remote testing
        cls.docker = docker.from_env()
        cls.docker.images.build(path='./test_environment/ubuntu-16', tag=cls.DOCKER_IMAGE_NAME)
        cls.containers = []

        for i in list(range(cls.TEST_HOST_COUNT)):
            container = cls.docker.containers.run(image=cls.DOCKER_IMAGE_NAME,
                                                  detach=True,
                                                  remove=True,
                                                  name=F"sshd-{i}",
                                                  auto_remove=True,
                                                  ports={'22/tcp': 8880 + i})
            cls.containers.append(container)
            # TODO: The IP of the server is semi-hardcoded. It should variable.
            mock_data.remote_test_data["plugins"][0]["props"]["host_address"].append(F"172.17.0.{2 + i}")

    def test_has_test_modules(self):
        self.assertGreater(len(self.plugin._modules), 0, "has at least one module")

    def test_testing_function(self):
        data = convert_test_input_json_to_dataclasses(mock_data.localhost_test_data)
        res = self.plugin_manager.launch_tests(data)
        self.assertTrue(res.total_count == 4)

    def test_remote_test(self):
        data = convert_test_input_json_to_dataclasses(mock_data.remote_test_data)
        res = self.plugin_manager.launch_tests(data)

        with self.subTest("a single module was executed"):
            self.assertEqual(1, res.total_count)
        with self.subTest(F"test run on {self.TEST_HOST_COUNT} hosts"):
            self.assertEqual(self.TEST_HOST_COUNT, len(res.plugin_result[0].module_result[0]['result_data'].items()))

    def test_password_removal(self):
        data = convert_test_input_json_to_dataclasses(mock_data.localhost_test_data)
        res = self.plugin_manager.launch_tests(data)
        self.assertEqual(res.plugin_result[0].props['password']['value'], "************")

    def test_multiple_host_testing(self):
        """
        TODO Implement
        :return:
        """
        self.assertTrue(True)

    @classmethod
    def tearDownClass(cls) -> None:
        for container in cls.containers:
            container.kill()
        cls.docker.close()


class PersistenceTest(unittest.TestCase):
    """
        I-4 - Persistenz von Daten
        """

    @classmethod
    def setUpClass(cls) -> None:
        cls.persistence = Persistence()
        cls.uuid = uuid.uuid4().hex

    def test_add_result_to_db(self):
        self.persistence.add_result(TestResult(self.uuid, "", "test_only", "", -1, -1, -1, "", datetime.now(), []))

    def test_get_result_from_db(self):
        res = self.persistence.Result.query.filter_by(id=self.uuid).first()
        self.assertTrue(res)


class PluginManagerTest(unittest.TestCase):
    """
    E-1 - Plugin-Manager
    """

    def test_serialize_and_deserialize(self):
        """
        Launch a test with two plugins
        Check if both results are in the output object
        :return:
        """
        data = convert_test_input_json_to_dataclasses(mock_data.local_test_with_two_plugins)
        with self.subTest(F"deserializes input data"):
            res = PluginManager().launch_tests(data)

        with self.subTest(F"serializes output data"):
            self.assertEqual(len(res.plugin_result), 2)

    def test_PluginManager(self):
        with self.subTest(F"has plugins"):
            self.assertTrue(len(PluginManager()._plugins) > 0)


class RestAPITest(unittest.TestCase):
    """
    S-1 - REST-API
    I-3 - Datenformate
    """

    def setUp(self) -> None:
        self.client = app.test_client()
        app.config['SECURE_API'] = False

    def test_api_swagger(self):
        response = self.client.get('/swagger.json')
        with self.subTest("'/swagger.json' exists"):
            self.assertTrue(response.status_code == 200)
        with self.subTest("data contains swagger json"):
            self.assertTrue('swagger' in response.get_json())
        with self.subTest("is version 2.0"):
            self.assertTrue('2.0' == response.get_json()['swagger'])

    def test_api_plugins(self):
        response = self.client.get('/plugins')
        with self.subTest("'/plugins' exists"):
            self.assertTrue(response.status_code == 200)
        with self.subTest("response format is valid"):
            self.assertIsNone(validate(response.get_json(), plugin_scheme))

    def test_api_flat_plugin_list(self):
        response = self.client.get('/plugins/flat')
        with self.subTest("'/plugins/flat' exists"):
            self.assertTrue(response.status_code == 200)
        with self.subTest("response format is valid"):
            self.assertIsNone(validate(response.get_json(), plugin_scheme))

    def tearDown(self) -> None:
        yield self.client


class RestAPIAuthenticationTest(unittest.TestCase):
    """
    S-2 - Implementierung einer Autorisierung
    """
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

    def test_working_authentication(self):
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

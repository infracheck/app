import unittest
import docker

from infracheck.Api import convert_test_input_json_to_dataclasses
from infracheck.PluginManager import PluginManager
from test import mock_data

DOCKER_IMAGE_NAME = 'ubuntu-sshd'
TEST_HOST_COUNT = 1  # Just a single host


class FunctionalPluginTest(unittest.TestCase):
    """
    E-4 - Integration eines Plugins
    P-1 - Integration von ssh- und winrm-Schnittstellen
    Sk-1 - Testen mehrerer Hosts
    """

    @classmethod
    def setUpClass(cls) -> None:
        plugin_id = "TestInfraPlugin"
        cls.plugin_manager = PluginManager()
        cls.plugin = cls.plugin_manager._get_plugin_instance(plugin_id)

        # Setup two containers for remote testing
        cls.docker = docker.from_env()
        cls.docker.images.build(path='../test_environment/ubuntu-16', tag=DOCKER_IMAGE_NAME)
        cls.containers = []

        for i in list(range(TEST_HOST_COUNT)):
            container = cls.docker.containers.run(image=DOCKER_IMAGE_NAME,
                                                  detach=True,
                                                  remove=True,
                                                  name=F"sshd-{i}",
                                                  auto_remove=True,
                                                  ports={'22/tcp': 8880 + i})
            cls.containers.append(container)

    def test_has_test_modules(self):
        self.assertGreater(len(self.plugin._modules), 0, "has at least one module")

    def test_testing_function(self):
        data = convert_test_input_json_to_dataclasses(mock_data.localhost_test_data)
        res = self.plugin_manager.launch_tests(data)
        self.assertTrue(res.total_count == 4)

    def test_remote_test(self):
        data = convert_test_input_json_to_dataclasses(mock_data.remote_test_data)
        res = self.plugin_manager.launch_tests(data)
        self.assertTrue(res.total_count == 1)

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

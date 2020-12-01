# This script can be used to measure the performance of the TestinfraPlugin
import timeit

import docker as docker

from infracheck.Api import convert_test_input_json_to_dataclasses
from infracheck.PluginManager import PluginManager
from test.test_performance import performance_mock
from test.test_performance.performance_mock import compare_module, service_module, os_module, address_module, \
    plugin_data

TEST_HOST_COUNT = 9

plugin_id = "TestInfraPlugin"
plugin_manager = PluginManager()
plugin = plugin_manager._get_plugin_instance(plugin_id)

# Setup two containers for remote testing
docker = docker.from_env()
docker.images.build(path='../test_environment/ubuntu-16', tag='ubuntu-sshd')
containers = []


def test_four_module():
    plugin_data["plugins"][0]["modules"] = [os_module, os_module, os_module, os_module]
    data = convert_test_input_json_to_dataclasses(plugin_data)
    plugin_manager.launch_tests(data)


def test_single_module():
    plugin_data["plugins"][0]["modules"] = [os_module]
    data = convert_test_input_json_to_dataclasses(plugin_data)
    plugin_manager.launch_tests(data)


def test_two_module():
    plugin_data["plugins"][0]["modules"] = [os_module, os_module]
    data = convert_test_input_json_to_dataclasses(plugin_data)
    plugin_manager.launch_tests(data)


def test_three_module():
    plugin_data["plugins"][0]["modules"] = [os_module, os_module, os_module]
    data = convert_test_input_json_to_dataclasses(plugin_data)
    plugin_manager.launch_tests(data)


if __name__ == '__main__':
    results = {}

    for i in list(range(TEST_HOST_COUNT)):
        container = docker.containers.run(image='ubuntu-sshd',
                                          detach=True,
                                          remove=True,
                                          name=F"sshd-{i}",
                                          auto_remove=True,
                                          ports={'22/tcp': 8880 + i})
        containers.append(container)
        # TODO: The IP of the server is semi-hardcoded. It should variable.
        plugin_data["plugins"][0]["props"]["host_address"].append(F"172.17.0.{2 + i}")

    # Tests
    print(F"{TEST_HOST_COUNT},1,"
          F"{timeit.timeit('test_single_module()', setup='from __main__ import test_single_module', number=2)}")

    print(F"{TEST_HOST_COUNT},2,"
          F"{timeit.timeit('test_two_module()', setup='from __main__ import test_two_module', number=2)}")

    print(F"{TEST_HOST_COUNT},3,"
          F"{timeit.timeit('test_three_module()', setup='from __main__ import test_three_module', number=2)}")

    print(F"{TEST_HOST_COUNT},4,"
          F"{timeit.timeit('test_four_module()', setup='from __main__ import test_four_module', number=2)}")

    # teardown
    for container in containers:
        container.kill()
    docker.close()

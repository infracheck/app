# This script can be used to measure the performance of the TestinfraPlugin
import timeit

import docker as docker

from infracheck.Api import convert_test_input_json_to_dataclasses, plugin_manager
from test.test_performance.performance_mock import plugin_data, service_module

HOST_COUNT = 200
MODULE_COUNT = 5

docker = docker.from_env()
docker.images.build(path='../test_environment/ubuntu-16', tag='ubuntu-sshd')


def test():
    data = convert_test_input_json_to_dataclasses(plugin_data)
    plugin_manager.launch_tests(data)


if __name__ == '__main__':
    containers = []
    for i in list(range(HOST_COUNT)):
        container = docker.containers.run(image='ubuntu-sshd',
                                          detach=True,
                                          remove=True,
                                          name=F"sshd-{i}",
                                          auto_remove=True,
                                          ports={'22/tcp': 8880 + i})
        containers.append(container)

    plugin_data["plugins"][0]["props"]["host_address"] = []
    print("host_count,module_count,time")

    for i in list(range(MODULE_COUNT)):
        plugin_data["plugins"][0]["modules"].append(service_module)

    for j in list(range(HOST_COUNT)):
        plugin_data["plugins"][0]["props"]["host_address"].append(F"172.17.0.{2 + j}")
    time = timeit.timeit('test()', setup='from __main__ import test', number=1)
    print(F"{j+1},{i+1},{time}")

    # teardown
    for container in containers:
        container.kill()
    docker.close()

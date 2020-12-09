from multiprocessing import Pool

from plugins.TestinfraPlugin.TestInfraConnector import Connection


# Some example code for multiprocessing

def _test(host):
    service = host.service("docker")
    return {
        "enabled": service.is_enabled,
        "running": service.is_running
    }


if __name__ == '__main__':
    hosts = []
    for i in list(range(10)):
        hosts.append(
            Connection('root', '172.17.0.2', 'password', 22, 'linux').host
        )

    # print([host.service("docker").is_enabled for host in hosts])

    with Pool(processes=10) as pool:
        multiple_results = [pool.apply_async(_test, (host,)) for host in hosts]
        results = ([res.get() for res in multiple_results])

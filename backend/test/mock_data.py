localhost_test_data = {
    "name": "Just another test",
    "description": "Hey there its me",
    "plugins": [
        {
            "id": "TestInfraPlugin",
            "props": {
                "host_address": ["localhost"],
                "username": "",
                "password": "",
                "os": "linux",
                "port": 22
            },
            "modules": [
                {
                    "id": "CheckTargetAddress",
                    "props": {
                        "url": "google.de"
                    }
                },
                {
                    "id": "CheckServiceSpecs",
                    "props": {
                        "type": "linux",
                        "distribution": "",
                        "release": "",
                        "codename": ""
                    }
                },
                {
                    "id": "CompareCommandOutput",
                    "props": {
                        "command1": "echo LOL",
                        "command2": "echo LOL"
                    }
                },
                {
                    "id": "CheckServiceSpecs",
                    "props": {
                        "service": "docker",
                        "enabled": True,
                        "running": True
                    }
                }
            ]
        }
    ]
}

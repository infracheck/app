localhost_test_data = {
    "label": "Just another test",
    "description": "Hey there its me",
    "plugins": [
        {
            "id": "TestInfraPlugin",
            "label": "My favorite Test on localhost",
            "props": {
                "host_address": [
                    "localhost"
                ],
                "username": "",
                "password": "",
                "os": "linux",
                "port": 22
            },
            "modules": [
                {
                    "id": "CheckTargetAddress",
                    "label": "Is Google reachable?",
                    "props": {
                        "url": "google.de"
                    }
                },
                {
                    "id": "CheckServiceSpecs",
                    "label": "Is it linux?",
                    "props": {
                        "type": "linux",
                        "distribution": "",
                        "release": "",
                        "codename": ""
                    }
                },
                {
                    "id": "CompareCommandOutput",
                    "label": "Is 'lol' == 'lol'",
                    "props": {
                        "command1": "echo LOL",
                        "command2": "echo LOL"
                    }
                },
                {
                    "id": "CheckServiceSpecs",
                    "label": "Does docker run?",
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

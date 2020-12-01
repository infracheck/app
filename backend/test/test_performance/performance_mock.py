plugin_data = {
    "label": "Just another test",
    "description": "Hey there its me",
    "plugins": [
        {
            "id": "TestInfraPlugin",
            "label": "My favorite Test on localhost",
            "props": {
                "host_address": [
                ],
                "username": "root",
                "password": "password",
                "os": "linux",
                "port": 22
            },
            "modules": [
            ]
        }
    ]
}

service_module = {
    "id": "CheckServiceSpecs",
    "label": "Is it linux?",
    "props": {
        "type": "linux",
        "distribution": "",
        "release": "",
        "codename": ""
    }
}

os_module = {
    "id": "CheckServiceSpecs",
    "label": "Is it linux?",
    "props": {
        "type": "linux",
        "distribution": "",
        "release": "",
        "codename": ""
    }
}
address_module = {
    "id": "CheckTargetAddress",
    "label": "Is yahoo reachable?",
    "props": {
        "url": "yahoo.com"
    }
}

compare_module = {
    "id": "CompareCommandOutput",
    "label": "Is 'lol' == 'lol'",
    "props": {
        "command1": "echo LOL",
        "command2": "echo LOL"
    }
}

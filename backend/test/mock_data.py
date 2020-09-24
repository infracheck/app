import datetime

from infracheck.model.TestResult import TestResult

result_mock: TestResult = {
    "id": "",
    "pdf_link": "",
    "name": "",
    "description": "",
    "success_count": 0,
    "failure_count": 0,
    "error_count": 0,
    "total_count": 0,
    "message": "",
    "date": datetime.datetime.now(),
    "plugin_result": []
}

test_data = {
    "name": "Just another test",
    "description": "Hey there its me",
    "plugins": [
        {
            "id": "demo_plugin",
            "params": {},
            "modules": [
                {
                    "id": "equality_check",
                    "params": {
                        "number1": 1,
                        "number2": 1
                    }
                }
            ]
        }
    ]
}

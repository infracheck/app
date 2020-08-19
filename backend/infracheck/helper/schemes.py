"""
This file contains all JSON schemes that can be send to the backend
"""

# This is how the input data, to launch a test, should look like
test_data_scheme = {
    "type": "object",
    "required": ["name", "description", "plugins"],
    "properties": {
        "name": {"type": "string"},
        "description": {"type": "string"},
        "plugins": {"type": "array",
                    "items": {
                        "type": "object",
                        "required": ["id", "params", "modules"],
                        "additionalProperties": True,
                        "properties": {
                            "id": {"type": "string"},
                            "params": {"type": "object"},
                            "modules": {"type": "array",
                                        "items": {
                                            "type": "object",
                                            "required": ["id", "params"],
                                            "additionalProperties": False,
                                            "properties": {
                                                "id": {"type": "string"},
                                                "params": {"type": "object"}
                                            }
                                        }
                                        }
                        }
                    }
                    }
    },
    "additionalProperties": False
}

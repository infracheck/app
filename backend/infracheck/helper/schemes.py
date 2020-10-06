"""
This file contains all JSON schemes that can be send to the backend
"""

# Scheme for /plugins route
# TODO: Implement properly
plugin_scheme = {
    "type": "object",
    "additionalProperties": True
}

# This is how the input data, to launch a test, should look like
test_data_scheme = {
    "type": "object",
    "required": ["name", "description", "plugins"],
    "properties": {
        "name": {"type": "string"},
        "description": {"type": "string"},
        "plugins": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["id", "props", "modules"],
                "additionalProperties": False,
                "properties": {
                    "id": {"type": "string"},
                    "props": {"type": "object"},
                    "modules": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["id", "props"],
                            "additionalProperties": False,
                            "properties": {
                                "id": {"type": "string"},
                                "props": {"type": "object"}
                            }
                        }
                    }
                }
            }
        }
    },
    "additionalProperties": False
}

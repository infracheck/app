"""
This file contains all JSON schemes that can be send to the backend
"""

# Scheme for /plugins route
# TODO: Implement properly
plugin_scheme = {
    "type": "object",
    "additionalProperties": True
}

module_result_scheme = {
    "type": "object",
    "required": [
        "result_successful",
        "result_message",
        "result_data",
        "module_name",
        "module_version",
        "props"
    ],
    "additionalProperties": False,
    "properties": {
        "result_successful": {"type": "boolean"},
        "result_message": {"type": "string"},
        "module_name": {"type": "string"},
        "module_version": {"type": "float"},
        "props": {"type": "object"},
        "result_data": {"type": "object"}
    }
}

plugin_result_scheme = {
    "type": "object",
    "required": [
        "failure_count",
        "success_count",
        "total_count",
        "module_result",
        "plugin_name",
        "plugin_version",
        "props"
    ],
    "additionalProperties": False,
    "properties": {
        "plugin_name": {"type": "string"},
        "plugin_version": {"type": "string"},
        "failure_count": {"type": "integer"},
        "success_count": {"type": "integer"},
        "total_count": {"type": "integer"},
        "props": {"type": "object"},
        "module_result": {
            "type": "array",
            "items": module_result_scheme
        }
    }
}

result_scheme = {
    "type": "object",
    "required": ["date", "id", "description", "failure_count", "success_count", "total_count", "message", "name",
                 "plugin_result"],
    "additionalProperties": False,
    "properties": {
        "id": {"type": "string"},
        "name": {"type": "string"},
        "date": {"type": "string"},
        "description": {"type": "string"},
        "failure_count": {"type": "integer"},
        "success_count": {"type": "integer"},
        "total_count": {"type": "integer"},
        "message": {"type": "string"},
        "plugin_result": {"type": "array",
                          "items": plugin_result_scheme}
    }
}
results_scheme = {
    "type": "array",
    "items": result_scheme
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

# LOGIN / LOGOUT

jwt_scheme = {
    "type": "object",
    "required": [
        "access_token",
        "refresh_token"
    ],
    "additionalProperties": False,
    "properties": {
        "access_token": {"type": "string"},
        "refresh_token": {"type": "string"},
    }
}

jwt_refresh_scheme = {
    "type": "object",
    "required": [
        "access_token",
    ],
    "additionalProperties": False,
    "properties": {
        "access_token": {"type": "string"},
    }
}

# PLUGIN

plugin_output_scheme = {
    "type": "object",
    "required": [
        "id", "props", "documentation", "author", "compatibility", "type", "version"
    ],
    "additionalProperties": False,
    "properties": {
        "author": {"type": "string"},
        "compatibility": {"type": "string"},
        "documentation": {"type": "string"},
        "id": {"type": "string"},
        "props": {"type": "object"},
        "type": {"type": "string"},
        "version": {"type": "float"},
        "modules": {"type": "object"},
    }
}

plugins_output_scheme = {
    "type": "array",
    "items": plugin_output_scheme
}

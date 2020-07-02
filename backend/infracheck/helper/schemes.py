test_data_scheme = {
    "type": "object",
    "required": ["name", "description", "plugins"],
    "properties": {
        "name": {"type": "string"},
        "description": {"type": "string"},
        "plugins": {"type": "array",
                    "items": {
                        "type": "object",
                        "required": ["id", "data", "modules"],
                        "additionalProperties": False,
                        "properties": {
                            "id": {"type": "string"},
                            "data": {"type": "object"},
                            "modules": {"type": "array",
                                        "items": {
                                            "type": "object",
                                            "required": ["id", "fields"],
                                            "additionalProperties": False,
                                            "properties": {
                                                "id": {"type": "string"},
                                                "fields": {"type": "object"}
                                            }
                                        }
                                        }
                        }
                    }
                    }
    },
    "additionalProperties": False
}


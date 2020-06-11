from typing import TypedDict, Dict


class TestModule(TypedDict):
    documentation: str = """
    THIS IS MY DOCUMENTATION
    """
    fields: Dict = {
        "Field1": "Field1COntent",
        "Field2": 3
    }

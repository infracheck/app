from typing import Dict


class DataTypes(Dict):
    """
    Defines all data types that are supported as inputs to tests
    """
    Text = "string"
    Number = "number"
    Boolean = "boolean"
    TextList = "Array<string>"
    NumberList = "Array<number>"

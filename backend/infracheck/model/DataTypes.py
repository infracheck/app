from typing import Dict


class DataTypes(Dict):
    """
    Defines all data types that are supported as inputs to tests
    """
    Text = "Type.String"
    Number = "Type.Number"
    Boolean = "Type.Boolean"
    TextList = "Type.Array<string>"
    NumberList = "Type.Array<number>"
    Password = "Type.Password"

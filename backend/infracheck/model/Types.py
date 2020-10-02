from typing import Dict


class Types(Dict):
    """
    Defines all data types that are supported as inputs to tests
    """
    Text = "Type.String"
    Number = "Type.Number"
    Boolean = "Type.Boolean"
    TextList = "Type.StringArray"
    NumberList = "Type.NumberArray"
    Password = "Type.Password"
    TextArea = "Type.TextArea"  # use to store a lot of text.

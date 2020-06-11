from enum import Enum


class FieldType(Enum):
    Text = "string"
    Number = "number"
    List = "array"
    Dict = "dict"

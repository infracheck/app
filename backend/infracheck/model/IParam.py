from typing import TypedDict, Any

from infracheck.model.DataTypes import DataTypes


class IParam(TypedDict):
    """
    This defines the structure of custom parameters, that are used in IModule and
    """
    type: DataTypes  # Type of the value
    value: Any  # default value (this will be overwritten if set in test definition)

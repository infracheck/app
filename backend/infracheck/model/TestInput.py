from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class ModuleInput:
    """
    This interface defines the data send to each module
    """
    id: str
    props: Dict[str, Any]


@dataclass
class PluginInput:
    """ Input Data for each plugin
    This interface defines the data that is send to each plugin
        - id of the plugin
        - plugin specific data
        - data for each module of the plugin
    """
    id: str
    props: Dict[str, any]
    modules: List[ModuleInput]


@dataclass
class TestInput:
    """ This data is send via the rest api and can be used in the test flow
    It stores:
        - test meta data (name, description)
        - A list of PluginDataObjects, one for each plugin that should be used for the test
    """
    name: str
    description: str
    plugins: List[PluginInput]

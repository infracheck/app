from dataclasses import dataclass
from typing import TypedDict, List, Dict, Any

"""
This file defines input data for tests
They provide basic interfaces and can be extended by plugins and its modules.

The following is a example of a valid <ITestData> object:
{ "name": "Hello World",
  "description": "Hey there its me",
  "plugins": [{
      "name": "TestInfraPlugin",
      "data": {
        "hosts": [
          "192.168.44.44"
        ],
        "username": "username",
        "password": "password",
        "target_os": "linux"
      },
      "modules": [{
          "name": "service",
          "fields": {
            "service": "nginx",
            "running": 0,
            "enabled": 0
}}]}]}
"""


@dataclass
class IModuleData(TypedDict):
    """
    This interface defines the data send to each module
    """
    id: str
    fields: Dict[str, Any]


@dataclass
class IGeneralPluginData(TypedDict):
    """ Plugin specific input data
    All attributes will be specified by the plugin
    Example: If you have a plugin that executes code on a remote host, you could add the following attributes:
        - host
        - username
        - password
    """
    pass


@dataclass
class IPluginData(TypedDict):
    """ Input Data for each plugin
    This interface defines the data that is send to each plugin
        - id of the plugin
        - plugin specific data
        - data for each module of the plugin
    """
    id: str
    data: IGeneralPluginData
    modules: List[IModuleData]


@dataclass
class ITestData(TypedDict):
    """ This data is send via the rest api and can be used in the test flow
    It stores:
        - test meta data (name, description)
        - A list of PluginDataObjects, one for each plugin that should be used for the test
    """
    name: str
    description: str
    plugins: List[IPluginData]

from typing import TypedDict, List, Dict, Any


class IModuleData(TypedDict):
    name: str
    version: str
    fields: Dict[str, Any]


class IGeneralPluginData(TypedDict):
    pass


class IPluginData(TypedDict):
    name: str
    version: str
    data: IGeneralPluginData
    modules: List[IModuleData]


class ITestData(TypedDict):
    """ This data is send via the rest api and can be used in the test flow

    """
    name: str
    description: str
    plugins: List[IPluginData]

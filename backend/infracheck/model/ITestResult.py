from typing import TypedDict, Any, List


class ITestResult(TypedDict, total=True):
    id: str
    pdf_link: str
    name: str
    description: str
    succeeded: int
    failures: int
    errors: int
    total: int
    message: str
    plugin_data: List[Any]


class IPluginResult(TypedDict, total=True):
    plugin_name: str
    plugin_version: float
    succeeded: int
    failures: int
    errors: int
    total: int
    message: str
    custom_data: Any

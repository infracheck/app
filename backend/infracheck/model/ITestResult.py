from datetime import datetime
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
    date: datetime
    plugin_data: List[Any]


class IPluginResult(TypedDict, total=True):
    plugin_name: str
    plugin_version: float
    succeeded: int
    failures: int
    errors: int
    total: int
    message: str
    module_data: List[Any]
    custom_data: Any


class IModuleResult(TypedDict, total=True):
    module_name: str
    module_version: float
    fields: Any
    success: bool
    message: str

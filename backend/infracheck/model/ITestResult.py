from datetime import datetime
from typing import TypedDict, Any, List


class IModuleResult(TypedDict, total=True):
    module_name: str
    module_version: float
    params: Any
    is_successful: bool
    message: str


class IPluginResult(TypedDict, total=True):
    plugin_name: str
    plugin_version: float
    success_count: int
    failure_count: int
    error_count: int
    total_count: int
    message: str
    module_result: List[IModuleResult]
    custom_data: Any


class ITestResult(TypedDict, total=True):
    id: str
    pdf_link: str
    name: str
    description: str
    success_count: int
    failure_count: int
    error_count: int
    total_count: int
    message: str
    date: datetime
    plugin_result: List[IPluginResult]

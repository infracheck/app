from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict


@dataclass
class ModuleResult:
    """
    Interface of the result that comes from any module
    """
    is_successful: bool
    message: str
    custom_data: Dict


@dataclass
class ModulePostResult(ModuleResult):
    """

    """
    module_name: str
    module_version: float
    props: Dict = field(default_factory=dict)


@dataclass
class PluginResult:
    plugin_name: str
    plugin_version: float
    success_count: int
    failure_count: int
    total_count: int
    message: str
    module_result: List[ModulePostResult]
    props: Dict = field(default_factory=dict)


@dataclass
class TestResult:
    id: str
    pdf_link: str
    name: str
    description: str
    success_count: int
    failure_count: int
    total_count: int
    message: str
    date: datetime
    plugin_result: List[PluginResult]

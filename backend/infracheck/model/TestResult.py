import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict


class ModuleResult:
    """
    Interface of the result that comes from any module
    """
    result_successful: bool = False
    result_message: str = ''
    result_data: Dict = {}
    module_name: str = ''
    module_version: float = 0.0
    props: Dict = {}

    def __init__(self, result_successful, result_message, result_data) -> None:
        self.result_successful = result_successful
        self.result_message = result_message
        self.result_data = result_data

    def json(self) -> json:
        return {
            "result_successful": self.result_successful,
            "result_message": self.result_message,
            "result_data": self.result_data,
            "module_name": self.module_name,
            "module_version": self.module_version,
            "props": self.props
        }


@dataclass
class PluginResult:
    plugin_name: str
    plugin_version: float
    success_count: int
    failure_count: int
    total_count: int
    message: str
    module_result: List[ModuleResult]
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

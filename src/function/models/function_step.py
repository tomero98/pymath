from typing import List

from .enums.step_type import StepType
from .help_data import HelpData
from .step_info_data import StepInfoData


class FunctionStep:
    def __init__(self, step_type: StepType, question: str, order: int, help_data_list: List[HelpData] = None,
                 step_info_data: StepInfoData = None):
        self.type = step_type
        self.question = question
        self.order = order
        self.help_data_list = help_data_list
        self.step_info_data = step_info_data

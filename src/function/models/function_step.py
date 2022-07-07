from .enums.inverse_step_type import InverseStepType
from .function_help_data import FunctionHelpData


class FunctionStep:
    def __init__(self, step_type: InverseStepType, question: str, order: int,
                 function_help_data: FunctionHelpData = None):
        self.type = step_type
        self.question = question
        self.order = order
        self.function_help_data = function_help_data

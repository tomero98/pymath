from typing import List

from .function import Function
from .function_point import FunctionPoint


class FunctionHelpData:
    def __init__(self, help_text: str, help_expressions: List[Function], help_points: List[FunctionPoint] = None):
        self.help_text = help_text
        self.help_expressions = help_expressions
        self.help_points = help_points

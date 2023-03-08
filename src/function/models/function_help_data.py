from typing import List

from .function import Function
from .function_point import FunctionPoint


class FunctionHelpData:
    def __init__(self, order: int, texts: List[str], functions: List[Function], points: List[FunctionPoint] = None):
        self.order = order
        self.texts = texts
        self.functions = functions
        self.points = points

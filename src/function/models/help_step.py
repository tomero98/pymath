from typing import List

from .function import Function
from .point import Point


class HelpStep:
    def __init__(self, order: int, functions: List[Function] = [], points: List[Point] = [], text: str = '',
                 function_color: str = '', point_color: str = ''):
        self.order = order
        self.functions = functions
        self.points = points
        self.text = text
        self.function_color = function_color
        self.point_color = point_color

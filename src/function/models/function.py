import math  # noqa
from typing import List


class Function:
    def __init__(self, function_id: int, expression: str, domain: [str, None], is_main_graphic: bool,
                 inverse_function: ['Function', None], is_invert: bool = False):
        self.function_id = function_id
        self.expression = expression
        self.domain = domain
        self.is_main_graphic = is_main_graphic
        self.inverse_function = inverse_function
        self._is_invert = is_invert

    def get_points(self) -> (List[int], List[int]):
        x_values = self._get_domain_values()
        y_values = [eval(self.expression.replace('x', str(x))) for x in x_values]
        return x_values, y_values

    def get_points_grouped(self) -> (List[int], List[int]):
        x_values = self._get_domain_values() if self.domain else range(-50, 50)
        points = [(x, eval(self.expression.replace('x', str(x)))) for x in x_values]
        return points

    def _get_domain_values(self):
        min_x, max_x = [int(expression) for expression in self.domain[1:-1].split(',')]
        return [num / 1000 for num in range(min_x * 1000, max_x * 1000, 1)]

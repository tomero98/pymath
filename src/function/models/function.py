import math  # noqa
from typing import List


class Function:
    def __init__(self, function_id: int, expression: str, domain: [str, None], is_main_graphic: bool,
                 is_elementary_graph: bool, inverse_function: ['Function', None], is_invert: bool = False):
        self.function_id = function_id
        self.expression = expression
        self.domain = domain
        self.is_main_graphic = is_main_graphic
        self.is_elementary_graph = is_elementary_graph
        self.inverse_function = inverse_function
        self.is_invert = is_invert

    def get_points(self, small_sample: bool = False) -> (List[int], List[int]):
        x_values = self._get_domain_values(small_sample=small_sample)
        y_values = self._get_range_values(x_values=x_values)
        return x_values, y_values

    def get_constant_points(self):
        min_x, max_x = self.domain[1:-1].split(',')
        min_x, max_x = float(min_x), float(max_x)
        min_y, max_y = [eval(self.expression.replace('x', str(x))) for x in (min_x, max_x)]
        if self.is_invert:
            min_x, min_y = min_y, min_x
            max_x, max_y = max_y, max_x
        return (min_x, max_x), (min_y, max_y)

    def _get_domain_values(self, small_sample: bool):
        value = 1000 if not small_sample else 10
        min_x, max_x = [int(expression) for expression in self.domain[1:-1].split(',')]
        return [num / value for num in range(min_x * value, max_x * value, 1)]

    def _get_range_values(self, x_values: List[float]):
        y_values = []
        x_value_to_del = []
        for x in x_values:
            try:
                y_values.append(eval(self.expression.replace('x', str(x))))
            except Exception:
                x_value_to_del.append(x)

        for x in x_value_to_del:
            x_values.remove(x)
        return y_values

    def get_center_point(self):
        random_points = self.get_random_points()
        return random_points[len(random_points) // 2]

    def get_random_points(self) -> (float, float):
        x_values, y_values = self.get_points(small_sample=True)
        filter_values = list(
            (x_value, y_value) for x_value, y_value in zip(x_values, y_values) if -2 < x_value < 4 and -2 < y_value < 4
        )
        return filter_values

    def get_points_grouped(self, small_sample: bool = False) -> (List[int], List[int]):
        x_values = self._get_domain_values(small_sample=small_sample) if self.domain else range(-50, 50)
        points = [(x, eval(self.expression.replace('x', str(x)))) for x in x_values]
        return points

    def get_points_range(self):
        x_values, y_values = self.get_points(small_sample=True)
        points = zip(x_values, y_values)
        return self.get_range(points=points)

    def get_range(self, points):
        point_range = []
        for x, y in points:
            x_range = (round(x - 0.2, 2), round(x + 0.2, 2))
            y_range = (round(y - 0.2, 2), round(y + 0.2, 2))
            point_range.append((x_range, y_range))
        return point_range

    def get_domain_function(self):
        x_start, x_end = self.domain[1: -1].split(',')
        x_start = int(x_start)
        x_end = int(x_end)
        x_start = x_start if -5 < x_start else '-inf'
        x_end = x_end if x_end < 5 else '+inf'
        start_interval = self.domain[0] if x_start != '-inf' else '('
        end_interval = self.domain[-1] if x_end != '+inf' else ')'
        return f'{start_interval}{x_start}, {x_end}{end_interval}'

    def get_range_function(self, exercise_domain: tuple):
        if self.expression.isnumeric():
            return self.expression

        x_values, y_values = self.get_points(small_sample=True)

        x_value_by_y_value = dict()
        y_values_filtered = list()
        for x_value, y_value in zip(x_values, y_values):
            if exercise_domain[0] <= x_value <= exercise_domain[1]:
                x_value_by_y_value[y_value] = x_value
                y_values_filtered.append(y_value)

        min_y, max_y = min(y_values_filtered), max(y_values_filtered)


        x_start, x_end = self.domain[1: -1].split(',')
        x_start = float(x_start)
        x_end = float(x_end)
        y_start = round(eval(self.expression.replace('x', str(x_start))), 2)
        y_start = y_start if -5 < y_start else '-inf'
        y_end = round(eval(self.expression.replace('x', str(x_end))), 2)
        y_end = y_end if y_end < 5 else '+inf'
        start_interval = self.domain[0] if y_start != '-inf' else '('
        end_interval = self.domain[-1] if y_end != '+inf' else ')'
        return f'{start_interval}{y_start}, {y_end}{end_interval}'

    def get_math_expression(self):
        return self.expression.replace('math.sqrt', '√').replace('**', '^').replace('math.e', 'e') \
            .replace('math.log', 'ln').replace('math.cosh', 'cosh').replace('math.cos', 'cos') \
            .replace('math.acos', 'acos').replace('math.sin', 'sin').replace('math.tan', 'tan') \
            .replace('math.asin', 'asin')

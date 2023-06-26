import math
from collections import defaultdict
from functools import lru_cache
from typing import List, Tuple

from sympy import symbols, limit, oo, diff, solve
from sympy.core.numbers import Rational


class Function:
    _PERIOD_BY_SPECIAL_FUNCTION_EXPRESSIONS = {
        'math.tan(x)': math.pi / 2,
        'math.cos(x)/math.sin(x)': math.pi,
        '1/math.sin(x)': math.pi,
        '1/math.cos(x)': math.pi / 2,
    }

    def __init__(self, function_id: int, expression: str, x_values_range: Tuple[int, int], is_main_graphic: bool,
                 domain: str = '', is_invert_function: bool = False):
        self.function_id = function_id
        self.expression = expression
        self.x_values_range = x_values_range
        self.is_main_graphic = is_main_graphic
        self.vertical_asymptotes = []
        self.horizontal_asymptotes = []
        self.x_values, self.y_values = [], []
        self.domain = domain
        self.real_range = ''
        self.is_invert_function = is_invert_function
        self.points = []

    def setup_data(self, plot_range: Tuple[int, int]):
        self.x_values, self.y_values = self.get_points(plot_range=plot_range)
        if self.is_invert_function:
            self.x_values, self.y_values = self.y_values, self.x_values

    def setup_domain_data(self, plot_range: Tuple[int, int]):
        self.setup_data(plot_range=plot_range)
        self.domain = self.get_domain(domain=self.domain)
        self.horizontal_asymptotes = self.get_horizontal_asymptotes()
        self.real_range = self.get_range_expression(plot_range=plot_range)

    @lru_cache(maxsize=2)
    def get_points(self, plot_range: Tuple[int, int] = (-5, 5)) -> (List[int], List[int]):
        all_x_values, all_y_values = [], []
        min_x, max_x = self.x_values_range[0], self.x_values_range[1]
        value = 100

        x_values, y_values = [], []
        range_value = [num / value for num in range(min_x * value, max_x * value + 1, 1)]
        for index, x_value in enumerate(range_value):
            try:
                y_value = eval(self.expression.replace('x', str(x_value)))

                x_values.append(x_value)
                y_values.append(y_value)
                is_included = True

                if index == 0:
                    if self.domain[0] != '[' and '-inf' not in self.domain:
                        is_included = False

                if index == len(range_value) - 1:
                    if self.domain[-1] != ']' and '+inf' not in self.domain:
                        is_included = False


                is_included = is_included if plot_range[0] <= y_value <= plot_range[1] else False
                self.points.append((x_value, y_value, is_included))
            except Exception as e:
                self.vertical_asymptotes.append(x_value)
                if x_values:
                    all_x_values.append(x_values)
                    all_y_values.append(y_values)
                    x_values, y_values = [], []

        if x_values:
            all_x_values.append(x_values)
            all_y_values.append(y_values)

        expression = self.expression.replace(' ', '').replace('+1', '').replace('-1', '')
        if expression in self._PERIOD_BY_SPECIAL_FUNCTION_EXPRESSIONS:
            all_x_values, all_y_values = self._get_special_function_values(
                all_x_value=all_x_values, all_y_values=all_y_values
            )
        return all_x_values, all_y_values

    def _get_special_function_values(self, all_x_value: list, all_y_values: list) -> [list, list]:
        expression_without_shifts = self.expression.replace(' ', '').replace('+1', '').replace('-1', '')
        period = self._PERIOD_BY_SPECIAL_FUNCTION_EXPRESSIONS[expression_without_shifts]
        if 'x + 1' in self.expression:
            shift = 1
        elif 'x - 1' in self.expression:
            shift = - 1
        else:
            shift = 0
        x_values_by_interval, y_values_by_interval = defaultdict(list), defaultdict(list)
        for x_point, y_point in zip(all_x_value, all_y_values):
            for x, y in zip(x_point, y_point):
                interval = int((x + shift) // period)
                x_values_by_interval[interval].append(x)
                y_values_by_interval[interval].append(y)

        x_values = []
        y_values = []
        for interval, x_value in x_values_by_interval.items():
            x_values.append(x_value)
            y_values.append(y_values_by_interval[interval])

        return x_values, y_values

    @lru_cache(maxsize=1)
    def get_domain(self, domain: str) -> str:
        if not self.vertical_asymptotes:
            return domain

        domain_parts = domain.split(',')
        return self._get_asymptote_domain(asymptotes=self.vertical_asymptotes, domain_parts=domain_parts)

    @lru_cache(maxsize=1)
    def get_range_expression(self, plot_range: Tuple[int, int]) -> str:
        range_parts = []
        all_y_values = [item for y_list in self.y_values for item in y_list]
        min_y, max_y = min(all_y_values), max(all_y_values)

        if len(set(all_y_values)) == 1:
            return f'[{min_y}, {max_y}]'

        if min_y < plot_range[0]:
            range_parts.append('(-inf')
        else:
            value = ''
            if min_y == all_y_values[0]:
                value = '[' if self.domain[0] == '[' or '-inf' in self.domain else '('
            if value != '[' and min_y == all_y_values[-1]:
                value = '[' if self.domain[-1] == ']' or '+inf' in self.domain else '('
            if not value:
                value = '['
            range_parts.append(f'{value}{min_y}')

        if max_y > plot_range[1]:
            range_parts.append(' +inf)')
        else:
            value = ''
            if max_y == all_y_values[0]:
                value = ']' if self.domain[0] == '[' or '-inf' in self.domain else ')'
            if value != ']' and max_y == all_y_values[-1]:
                value = ']' if self.domain[-1] == ']' or '+inf' in self.domain else ')'
            if not value:
                value = ']'
            range_parts.append(f' {max_y}{value}')

        if not self.horizontal_asymptotes:
            return ','.join(range_parts)
        else:
            return self._get_asymptote_domain(asymptotes=self.horizontal_asymptotes, domain_parts=range_parts)

    def _get_asymptote_domain(self, asymptotes: List[int], domain_parts: List[str]) -> str:
        asymptotes = sorted(asymptotes)
        asymptote_domains_list = []
        for index, asymptote in enumerate(asymptotes[:-1]):
            asymptote_domain = f'({asymptote}, {asymptotes[index + 1]})'
            asymptote_domains_list.append(asymptote_domain)

        asymptote_domains = ' U '.join(asymptote_domains_list)
        if asymptote_domains:
            return f'{domain_parts[0]}, {asymptotes[0]}) U {asymptote_domains} U ({asymptotes[-1]},{domain_parts[-1]}'
        else:
            return f'{domain_parts[0]}, {asymptotes[0]}) U ({asymptotes[-1]},{domain_parts[-1]}'

    @lru_cache(maxsize=1)
    def get_horizontal_asymptotes(self) -> List:
        sympy_expression = self.get_sympy_expression()
        if 'cos' in sympy_expression or 'sin' in sympy_expression:
            return []

        asymptotes = []
        asymptote_one = limit(sympy_expression, symbols('x'), -oo)
        if isinstance(asymptote_one, Rational):
            asymptotes.append(round(float(asymptote_one), 2))
        asymptote_two = limit(sympy_expression, symbols('x'), oo)
        if asymptote_one != asymptote_two and isinstance(asymptote_two, Rational):
            asymptotes.append(round(float(asymptote_two), 2))

        return asymptotes

    @lru_cache(maxsize=1)
    def get_maximum_minimum_points(self, plot_range: Tuple[float, float]) -> [List, Tuple, List, Tuple]:
        x_symbol = symbols('x')
        first_derivative = diff(self.expression, x_symbol)
        roots = solve(first_derivative, x_symbol)
        roots = [root for root in roots if plot_range[0] < round(float(root), 2) < plot_range[1]]

        maximum_values = []
        minimum_values = []
        second_derivative = diff(first_derivative, x_symbol)
        for root in roots:
            second_derivative_value = round(float(second_derivative.subs(x_symbol, root)), 2)
            if second_derivative_value:
                x_value = str(round(float(root), 2))
                y_value = eval(self.expression.replace('x', x_value))
                minimum_values.append((float(x_value), float(y_value)))
            elif second_derivative_value < 0:
                x_value = str(round(float(root), 2))
                y_value = eval(self.expression.replace('x', x_value))
                maximum_values.append((float(x_value), float(y_value)))

        maximum = None
        maximum_absolute = None
        for value in maximum_values:
            if value[1] == maximum:
                maximum_absolute = None

            if maximum is None or value[1] > maximum:
                maximum = value[1]
                maximum_absolute = value

        if maximum_absolute:
            maximum_values = [value for value in maximum_values if value[0] != maximum_absolute[0]]

        minimum = None
        minimum_absolute = None
        for value in minimum_values:
            if value[1] == minimum:
                minimum_absolute = None

            if minimum is None or value[1] < minimum:
                minimum = value[1]
                minimum_absolute = value
        if minimum_absolute:
            minimum_values = [value for value in maximum_values if value[0] != minimum_absolute[0]]

        return maximum_values, maximum_absolute, minimum_values, minimum_absolute

    def get_label_point(self) -> list:
        x_values = []
        y_values = []
        for x_group, y_group in zip(self.x_values, self.y_values):
            for x, y in zip(x_group, y_group):
                valid_x = self.x_values_range[0] <= x <= self.x_values_range[-1]
                valid_y = self.x_values_range[0] <= y <= self.x_values_range[-1]
                if valid_x and valid_y:
                    x_values.append(x)
                    y_values.append(y)

        num = len(x_values) // 5

        center_value = x_values[num * 3], y_values[num * 3] + 0.5
        left_value = x_values[num * 4], y_values[num * 4] + 0.5
        right_value = x_values[num * 2], y_values[num * 2] + 0.5
        return [center_value, left_value, right_value]

    def get_math_expression(self) -> str:
        return self.expression.replace('(math.e**x - math.e**(-x)) / 2', 'Sh(x)') \
            .replace('(math.e**(x + 1) - math.e**(-(x + 1))) / 2', 'Sh(x + 1)') \
            .replace('(math.e**(x - 1) - math.e**(-(x - 1))) / 2', 'Sh(x - 1)') \
            .replace('(math.e**x + math.e**(-x)) / 2', 'Ch(x)') \
            .replace('(math.e**(x + 1) + math.e**(-(x + 1))) / 2', 'Ch(x + 1)') \
            .replace('(math.e**(x - 1) + math.e**(-(x - 1))) / 2', 'Ch(x - 1)') \
            .replace('(math.e**x - math.e**(-x)) / (math.e**x + math.e**(-x))', 'Th(x)') \
            .replace('(math.e**(x + 1) - math.e**(-(x + 1))) / (math.e**(x + 1) + math.e**(-(x + 1)))', 'Th(x + 1)') \
            .replace('(math.e**(x - 1) - math.e**(-(x - 1))) / (math.e**(x - 1) + math.e**(-(x - 1)))', 'Th(x - 1)') \
            .replace('math.cos(x) / math.sin(x)', 'cot(x)') \
            .replace('math.cos(x + 1) / math.sin(x + 1)', 'cot(x + 1)') \
            .replace('math.cos(x - 1) / math.sin(x - 1)', 'cot(x - 1)') \
            .replace('1 / math.sin(x)', 'csc(x)') \
            .replace('1 / math.sin(x + 1)', 'csc(x + 1)') \
            .replace('1 / math.sin(x - 1)', 'csc(x - 1)') \
            .replace('1 / math.cos(x)', 'sec(x)') \
            .replace('1 / math.cos(x + 1)', 'sec(x + 1)') \
            .replace('1 / math.cos(x - 1)', 'sec(x -1)') \
            .replace('(x)**', 'x**').replace('**2', '²').replace('**3', '³').replace('math.sqrt', '√') \
            .replace('**', '^').replace('math.e', 'e').replace('math.log', 'ln').replace('math.cosh', 'cosh') \
            .replace('math.cos', 'cos').replace('math.acos', 'acos').replace('math.sin', 'sin') \
            .replace('math.tan', 'tan').replace('math.asin', 'asin')

    def get_sympy_expression(self) -> str:
        return self.expression.replace('math.e', 'E').replace('math.tan', 'tan').replace('math.log', 'log')

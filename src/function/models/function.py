import math  # noqa
from functools import lru_cache
from typing import List, Tuple

from sympy import symbols, limit, oo, diff, solve
from sympy.core.numbers import Rational


class Function:
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

    def setup_data(self, plot_range: Tuple[int, int]):
        print(self.expression)
        self.x_values, self.y_values = self.get_points()
        if self.is_invert_function:
            self.x_values, self.y_values = self.y_values, self.x_values

    def setup_domain_data(self, plot_range: Tuple[int, int]):
        self.setup_data(plot_range=plot_range)
        self.domain = self.get_domain(domain=self.domain)
        self.horizontal_asymptotes = self.get_horizontal_asymptotes()
        self.real_range = self.get_range_expression(plot_range=plot_range)

    @lru_cache(maxsize=2)
    def get_points(self) -> (List[int], List[int]):
        all_x_values, all_y_values = [], []
        min_x, max_x = self.x_values_range[0], self.x_values_range[1]
        value = 10

        x_values, y_values = [], []
        for x_value in [num / value for num in range(min_x * value, max_x * value + 1, 1)]:
            try:
                y_value = eval(self.expression.replace('x', str(x_value)))

                x_values.append(x_value)
                y_values.append(y_value)
            except Exception:
                self.vertical_asymptotes.append(x_value)
                if x_values:
                    all_x_values.append(x_values)
                    all_y_values.append(y_values)
                    x_values, y_values = [], []

        if x_values:
            all_x_values.append(x_values)
            all_y_values.append(y_values)
        return all_x_values, all_y_values

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

    ########################################################################################################################
    ########################################################################################################################
    ########################################################################################################################
    ########################################################################################################################
    ########################################################################################################################
    ########################################################################################################################

    def get_constant_points(self):
        min_x, max_x = self.x_values_range[1:-1].split(',')
        min_x, max_x = float(min_x), float(max_x)
        min_y, max_y = [eval(self.expression.replace('x', str(x))) for x in (min_x, max_x)]
        if self.is_invert:
            min_x, min_y = min_y, min_x
            max_x, max_y = max_y, max_x
        return (min_x, max_x), (min_y, max_y)

    def get_label_point(self, position: str = 'left'):
        num = len(self.x_values) // 6

        if position == 'left_plus':
            multiply = 2
        elif position == 'left':
            multiply = 3
        elif position == 'right':
            multiply = 4
        elif position == 'right_plus':
            multiply = 5
        return self.x_values[num * multiply] + 0.25, self.y_values[num * multiply] + 0.25

    def get_random_points(self) -> (float, float):
        x_values, y_values = self.get_points()
        filter_values = list(
            (x_value, y_value) for x_value, y_value in zip(x_values, y_values) if -2 < x_value < 4 and -2 < y_value < 4
        )
        return filter_values

    def get_math_expression(self) -> str:
        return self.expression.replace('(x)**', 'x**').replace('**2', '²').replace('**3', '³').replace('math.sqrt', '√') \
            .replace('**', '^').replace('math.e', 'e').replace('math.log', 'ln').replace('math.cosh', 'cosh') \
            .replace('math.cos', 'cos').replace('math.acos', 'acos').replace('math.sin', 'sin') \
            .replace('math.tan', 'tan').replace('math.asin', 'asin')

    def get_sympy_expression(self) -> str:
        return self.expression.replace('math.e', 'E').replace('math.tan', 'tan').replace('math.log', 'log')

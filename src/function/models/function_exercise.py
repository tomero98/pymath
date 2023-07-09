from collections import defaultdict
from functools import lru_cache
from typing import List, Tuple

from .point import Point
from .enums.function_exercise_type import FunctionExerciseType
from .function import Function
from .function_step import FunctionStep


class FunctionExercise:
    def __init__(self, identifier: int, exercise_type: str, title: str, plot_range: Tuple[int, int],
                 exercise_order: int, functions: List[Function], steps: List[FunctionStep],
                 exercise_points: List[Point] = []):
        self.id = identifier
        self.type = exercise_type
        self.title = title
        self.plot_range = plot_range
        self.exercise_order = exercise_order
        self.functions = functions
        self.steps = steps
        self.exercise_points = exercise_points

    @classmethod
    def get_title_by_exercise_type(cls, exercise_type) -> str:
        if exercise_type == FunctionExerciseType.inverse_graph_exercise.value:
            title = 'Funciones inversas'
        elif exercise_type == FunctionExerciseType.domain_concept_exercise.value:
            title = 'Dominio y recorrido'
        elif exercise_type == FunctionExerciseType.elementary_graph_exercise.value:
            title = 'Gráficas elementales'
        elif exercise_type == FunctionExerciseType.maximum_minimum_exercise.value:
            title = 'Máximos y Mínimos'
        return title

    @lru_cache(maxsize=1)
    def has_main_function_inverse(self) -> bool:
        main_function = self.get_main_function()[0]
        _, y_values = main_function.get_points()
        y_values = [y for y_group in y_values for y in y_group]
        return len(set(y_values)) == len(y_values)

    def get_main_function(self) -> List:
        return [function for function in self.functions if function.is_main_graphic]

    @lru_cache(maxsize=1)
    def get_maximum_minimum_points(self):
        max_points = []
        min_points = []
        maximum_minimum_points_by_type = defaultdict(list)
        included_points_by_x_value = {
            point.x: (point.x, point.y, point.is_included) for point in self.exercise_points if point.is_included
        }
        functions = sorted(self.functions, key=lambda function: function.x_values_range[0])
        sorted_functions = []
        constant_functions = []
        for function in functions:
            if function.expression.isdigit():
                constant_functions.append(function)
            else:
                sorted_functions.append(function)

        all_points_by_x_value = {}
        for function in sorted_functions:
            for point in function.points:
                if point[0] in all_points_by_x_value and point[2]:
                    all_points_by_x_value[point[0]] = point
                else:
                    all_points_by_x_value[point[0]] = point

        all_points_by_x_value.update(included_points_by_x_value)

        for x_value, point in all_points_by_x_value.items():
            if not max_points:
                max_points.append(point)
            elif max_points[0][1] == point[1]:
                max_points.append(point)
            elif max_points[0][1] < point[1]:
                max_points = [point]

            if not min_points:
                min_points.append(point)
            elif min_points[0][1] == point[1]:
                min_points.append(point)
            elif min_points[0][1] > point[1]:
                min_points = [point]

            if not point[2]:
                continue

            if int(point[0]) != point[0] and int(point[0]) + 0.5 != point[0]:
                continue

            previous_point = all_points_by_x_value.get(round(x_value - 0.01, 3))
            next_point = all_points_by_x_value.get(round(x_value + 0.01, 3))

            is_minimum_value = True
            is_maximum_value = True
            if previous_point:
                is_minimum_value = previous_point[1] > point[1]
                is_maximum_value = previous_point[1] < point[1]

            if next_point:
                is_minimum_value = next_point[1] > point[1] and is_minimum_value
                is_maximum_value = next_point[1] < point[1] and is_maximum_value

            if is_minimum_value:
                maximum_minimum_points_by_type['minimum'].append(point)
            if is_maximum_value:
                maximum_minimum_points_by_type['maximum'].append(point)

        self._constant_functions_max_min_points(
            constant_functions=constant_functions, all_points_by_x_value=all_points_by_x_value,
            max_points=max_points, min_points=min_points, maximum_minimum_points_by_type=maximum_minimum_points_by_type
        )

        maximum_relative_points = [
            (point[0], point[1])
            for point in maximum_minimum_points_by_type['maximum']
            if not max_points or max_points[0][1] != point[1]
        ]
        minimum_relative_points = [
            (point[0], point[1])
            for point in maximum_minimum_points_by_type['minimum']
            if not min_points or min_points[0][1] != point[1]
        ]

        max_points = [
            (point[0], point[1]) for point in max_points
            if point[2] and (int(point[1]) == point[1] or int(point[1]) + 0.5 == point[1])
        ]
        min_points = [
            (point[0], point[1]) for point in min_points
            if point[2] and (int(point[1]) == point[1] or int(point[1]) + 0.5 == point[1])
        ]
        return {
            'máximo absoluto': set(max_points) if max_points else None,
            'máximo relativo': set(maximum_relative_points) if maximum_relative_points else None,
            'mínimo absoluto': set(min_points) if min_points else None,
            'mínimo relativo': set(minimum_relative_points) if minimum_relative_points else None,
        }

    def _constant_functions_max_min_points(self, constant_functions: List[Function], all_points_by_x_value: dict,
                                           max_points: list, min_points: list, maximum_minimum_points_by_type: dict):
        const_max_points = []
        const_min_points = []
        for function in constant_functions:
            first_point = function.points[0]
            if first_point[2]:
                previous_point = all_points_by_x_value.get(round(first_point[0] - 0.01, 3))

                is_minimum_value = True
                is_maximum_value = True
                if previous_point:
                    is_minimum_value = previous_point[1] > first_point[1]
                    is_maximum_value = previous_point[1] < first_point[1]

                if is_minimum_value:
                    const_min_points.append(first_point)
                if is_maximum_value:
                    const_max_points.append(first_point)

            const_max_points.extend(function.points[1: -1])
            const_min_points.extend(function.points[1: -1])

            last_point = function.points[-1]
            if last_point[2]:
                next_point = all_points_by_x_value.get(round(last_point[0] + 0.01, 3))

                is_minimum_value = True
                is_maximum_value = True
                if next_point:
                    is_minimum_value = next_point[1] > last_point[1]
                    is_maximum_value = next_point[1] < last_point[1]

                if is_minimum_value:
                    const_min_points.append(last_point)
                if is_maximum_value:
                    const_max_points.append(last_point)

            maximum_minimum_points_by_type['maximum'].extend(const_max_points)
            maximum_minimum_points_by_type['minimum'].extend(const_min_points)

            if not max_points:
                max_points.extend(const_max_points)
            elif max_points[0][1] == first_point[1]:
                max_points.extend(const_max_points)
            elif max_points[0][1] < first_point[1]:
                max_points = const_max_points

            if not min_points:
                min_points.extend(const_min_points)
            elif min_points[0][1] == first_point[1]:
                min_points.extend(const_min_points)
            elif min_points[0][1] > first_point[1]:
                min_points = const_min_points

    def validate_domain_expression(self, user_domain_input: str) -> [bool, set]:
        exercise_domain = self.get_domain_expression()
        if user_domain_input == exercise_domain:
            return True, set(), set()

        user_domain_expression_set = set(user_domain_input.replace(' ', '').split('U'))
        exercise_domain_expression_set = set(exercise_domain.replace(' ', '').split('U'))
        if user_domain_expression_set == exercise_domain_expression_set:
            return True, set(), set()

        exercise_domain_set = set()
        for function in self.functions:
            function_domain = self.get_num_set_from_domain_expression(domain_expression=function.domain)
            exercise_domain_set.update(function_domain)

        user_domain_set = set()
        if user_domain_input:
            for domain_part in user_domain_input.split(' U '):
                user_domain_set.update(self.get_num_set_from_domain_expression(domain_expression=domain_part))

        return exercise_domain_set == user_domain_set, user_domain_set - exercise_domain_set, \
               exercise_domain_set - user_domain_set

    def get_domain_expression(self) -> str:
        return ' U '.join(function.domain for function in self.functions)

    def get_num_set_from_domain_expression(self, domain_expression: str) -> set:
        domain_num_set = set()
        domain_parts = domain_expression.split(' U ')
        for domain_part in domain_parts:
            limits = domain_part[1:-1].replace(',', '').split()
            if '-inf' not in limits[0]:
                lower_limit = round(float(limits[0]), 2)
            else:
                lower_limit = self.plot_range[0]

            if 'inf' not in limits[1]:
                upper_limit = round(float(limits[1]), 2)
            else:
                upper_limit = self.plot_range[1]

            values = [num / 10 for num in range(int(lower_limit * 10), int(upper_limit * 10) + 1, 1)]

            if domain_part[0] == '(' and '-inf' not in limits[0]:
                values = values[1:]

            if domain_part[-1] == ')' and 'inf' not in limits[1]:
                values = values[:-1]

            domain_num_set.update(values)
        return domain_num_set

    def validate_range_expression(self, user_range_input: str) -> [bool, set]:
        exercise_range = self.get_range_expression()
        if user_range_input == exercise_range:
            return True, set(), set()

        user_range_expression_set = set(user_range_input.replace(' ', '').split('U'))
        exercise_range_expression_set = set(exercise_range.replace(' ', '').split('U'))
        if user_range_expression_set == exercise_range_expression_set:
            return True, set(), set()

        exercise_range_set = set()
        for function in self.functions:
            range_domain = self.get_num_set_from_range_expression(range_expression=function.real_range)
            exercise_range_set.update(range_domain)

        user_range_set = set()
        if user_range_input:
            for range_part in user_range_input.split(' U '):
                user_range_set.update(self.get_num_set_from_range_expression(range_expression=range_part))
        return exercise_range_set == user_range_set, user_range_set - exercise_range_set, \
               exercise_range_set - user_range_set

    def get_range_expression(self) -> str:
        return ' U '.join(function.real_range for function in self.functions)

    def get_num_set_from_range_expression(self, range_expression: str) -> set:
        range_num_set = set()
        range_parts = range_expression.split(' U ')
        for range_part in range_parts:
            limits = range_part[1:-1].replace(',', '').split()
            if '-inf' not in limits[0]:
                lower_limit = round(float(limits[0]), 2)
            else:
                lower_limit = self.plot_range[0]

            if 'inf' not in limits[1]:
                upper_limit = round(float(limits[1]), 2)
            else:
                upper_limit = self.plot_range[1]

            values = [num / 10 for num in range(int(lower_limit * 10), int(upper_limit * 10) + 1, 1)]

            if range_part[0] == '(' and '-inf' not in limits[0]:
                values = values[1:]

            if range_part[-1] == ')' and 'inf' not in limits[1]:
                values = values[:-1]

            range_num_set.update(values)
        return range_num_set

    ####################################################################################################################
    ####################################################################################################################
    ####################################################################################################################
    ####################################################################################################################
    ####################################################################################################################

    def get_function_by_expression(self, expression: str) -> Function:
        function = next(function for function in self.functions if function.expression == expression)
        return function

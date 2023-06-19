from functools import lru_cache
from typing import List, Tuple

from .enums.function_exercise_type import FunctionExerciseType
from .function import Function
from .function_step import FunctionStep


class FunctionExercise:
    def __init__(self, identifier: int, exercise_type: str, title: str, plot_range: Tuple[int, int],
                 exercise_order: int, functions: List[Function], steps: List[FunctionStep]):
        self.id = identifier
        self.type = exercise_type
        self.title = title
        self.plot_range = plot_range
        self.exercise_order = exercise_order
        self.functions = functions
        self.steps = steps

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
        main_function = self.get_main_function()
        _, y_values = main_function.get_points()
        y_values = [y for y_group in y_values for y in y_group]
        return len(set(y_values)) == len(y_values)

    def get_main_function(self) -> Function:
        return next(function for function in self.functions if function.is_main_graphic)

    def _get_maximum_minimum_points(self):
        return [
            function.get_maximum_minimum_points(plot_range=self.plot_range)
            for function in self.functions if function.is_main_graphic
        ]

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

        user_domain_set = self.get_num_set_from_domain_expression(domain_expression=user_domain_input)
        return exercise_domain_set == user_domain_set, \
               user_domain_set - exercise_domain_set, \
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

    ####################################################################################################################
    ####################################################################################################################
    ####################################################################################################################
    ####################################################################################################################
    ####################################################################################################################

    def get_function_by_expression(self, expression: str) -> Function:
        function = next(function for function in self.functions if function.expression == expression)
        return function

    def validate_range_expression(self, range_expression: str):
        function_range = self.get_range_expression()
        return function_range.replace(' ', '') == range_expression.replace(' ', '')

    def get_range_expression(self):
        function_range = ' U '.join(
            function.get_range_function(plot_range=self.plot_range) for function in self.functions
        )
        return function_range

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
        elif exercise_type == FunctionExerciseType.maximum_points_exercise.value:
            title = 'Máximos'
        elif exercise_type == FunctionExerciseType.minimum_points_exercise.value:
            title = 'Mínimos'
        return title

    @lru_cache(maxsize=1)
    def has_main_function_inverse(self) -> bool:
        main_function = self.get_main_function()
        _, y_values = main_function.get_points()
        return len(set(y_values)) == len(y_values)

    def get_main_function(self) -> Function:
        return next(function for function in self.functions if function.is_main_graphic)

    def _get_maximum_minimum_points(self):
        pass

    ####################################################################################################################
    ####################################################################################################################
    ####################################################################################################################
    ####################################################################################################################
    ####################################################################################################################

    def get_function_by_expression(self, expression: str) -> Function:
        function = next(function for function in self.functions if function.expression == expression)
        return function

    def get_domain_range_values(self, small_sample: bool = False) -> (list, list):
        # Domain exercise
        functions = [function for function in self.functions if function.is_main_graphic]
        all_x_values = []
        all_y_values = []
        for function in functions:
            x_values, y_values = function.get_points()
            all_x_values.extend(x_values)
            all_y_values.extend(y_values)
        return all_x_values, all_y_values

    def validate_domain_expression(self, domain_expression: str):
        domain = self.get_domain_expression().replace(' ', '')
        domain_expression = domain_expression.replace(' ', '')
        domain_expression_list = domain_expression.split('U')
        return all(expression and expression in domain for expression in domain_expression_list)

    def validate_range_expression(self, range_expression: str):
        function_range = self.get_range_expression()
        return function_range.replace(' ', '') == range_expression.replace(' ', '')

    def get_domain_expression(self):
        domain = ' U '.join(function.get_domain_function() for function in self.functions)
        return domain

    def get_range_expression(self):
        function_range = ' U '.join(
            function.get_range_function(plot_range=self.plot_range) for function in self.functions
        )
        return function_range

    def has_bounded_range(self):
        return 'inf' not in self.get_range_expression()

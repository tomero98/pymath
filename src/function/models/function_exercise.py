from typing import List

from .enums.inverse_exercise_type import FunctionExerciseType
from .enums.step_type import StepType
from .function import Function
from .function_step import FunctionStep


class FunctionExercise:
    def __init__(self, identifier: int, exercise_type: str, title: str, exercise_domain: tuple, exercise_order: int,
                 functions: List[Function], steps: List[FunctionStep]):
        self.id = identifier
        self.type = exercise_type
        self.title = title
        self.exercise_domain = exercise_domain
        self.exercise_order = exercise_order
        self.functions = functions
        self.steps = steps

    ####################################################################################################################
    ####################################################################################################################
    ####################################################################################################################
    ####################################################################################################################
    ####################################################################################################################

    def has_main_function_inverse(self) -> bool:
        main_function = next(function for function in self.functions if function.is_main_graphic)
        _, y_values = main_function.get_points()
        return len(set(y_values)) == len(y_values)

    def get_inverse_graph(self) -> Function:
        main_function = next(function for function in self.functions if function.is_main_graphic)
        return main_function.inverse_function

    def get_main_function(self) -> Function:
        main_function = next(function for function in self.functions if function.is_main_graphic)
        return main_function

    def get_function_by_expression(self, expression: str) -> Function:
        function = next(function for function in self.functions if function.expression == expression)
        return function

    def get_domain_range_values(self, small_sample: bool = False) -> (list, list):
        # Domain exercise
        functions = [function for function in self.functions if function.is_main_graphic]
        all_x_values = []
        all_y_values = []
        for function in functions:
            x_values, y_values = function.get_points(small_sample=small_sample)
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
            function.get_range_function(exercise_domain=self.exercise_domain) for function in self.functions
        )
        return function_range

    def has_bounded_range(self):
        return 'inf' not in self.get_range_expression()

    def get_maximum_minimum_value(self, step_type) -> str:
        points = []
        for function in self.functions:
            points.extend(function.get_points_range())
        if step_type == StepType.maximum_absolute_exercise:
            value = self._get_maximum_absolute_value(points=points)
        elif step_type == StepType.maximum_relative_exercise:
            value = self._get_maximum_relative_value(points=points)
        elif step_type == StepType.minimum_absolute_exercise:
            value = self._get_minimum_absolute_value(points=points)
        else:
            value = self._get_minimum_relative_value(points=points)
        return value

    def _get_maximum_absolute_value(self, points: list):
        pass

    def _get_maximum_relative_value(self, points: list):
        pass

    def _get_minimum_absolute_value(self, points: list):
        pass

    def _get_minimum_relative_value(self, points: list):
        pass

    @classmethod
    def get_title_by_exercise_type(cls, exercise_type) -> str:
        if exercise_type == FunctionExerciseType.inverse_concept_exercise.value:
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

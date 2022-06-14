from functools import reduce
from typing import List

from .function import Function
from .function_step import FunctionStep


class FunctionExercise:
    def __init__(self, identifier: int, exercise_type: str, title: str, exercise_order: int, exercise_priority: int,
                 functions: List[Function], steps: List[FunctionStep]):
        self.id = identifier
        self.type = exercise_type
        self.title = title
        self.exercise_order = exercise_order
        self.exercise_priority = exercise_priority
        self.functions = functions
        self.steps = steps

    def get_points_of_first_graph(self) -> (List[int], List[int]):
        function = self.functions[0]
        x_values, y_values = function.get_points()
        return x_values, y_values

    def has_main_function_inverse(self) -> bool:
        main_function = next(function for function in self.functions if function.is_main_graphic)
        return True

    def get_inverse_graph(self) -> Function:
        main_function = next(function for function in self.functions if function.is_main_graphic)
        return main_function.inverse_function

    def get_main_function(self) -> Function:
        main_function = next(function for function in self.functions if function.is_main_graphic)
        return main_function

    def get_all_points_not_duplicated(self, include_main_graphic: bool = True,
                                      include_inverse_points: bool = False) -> set:
        points_list = [
            set(function.get_points_grouped()) for function in self.functions
            if not include_main_graphic and not function.is_main_graphic
        ]
        if include_inverse_points:
            main_function = next(function for function in self.functions if function.is_main_graphic)
            inverse_function = main_function.inverse_function
            points_list.append(set(inverse_function.get_points_grouped()))

        points = reduce(lambda a, b: a.symmetric_difference(b), points_list)
        return points

    def get_domain_values(self):
        functions = [function for function in self.functions if function.is_main_graphic]
        all_x_values = []
        all_y_values = []
        for function in functions:
            x_values, y_values = function.get_points()
            all_x_values.extend(x_values)
            all_y_values.extend(y_values)

        return all_x_values, all_y_values

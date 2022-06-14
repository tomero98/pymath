from typing import List

from ..models.enums.inverse_step_type import InverseStepType
from ..models.function import Function
from ..models.function_exercise import FunctionExercise
from ..models.function_help_data import FunctionHelpData


class HelpDataMapper:
    def get_help_data(self, exercise: FunctionExercise, step_type: InverseStepType) -> FunctionHelpData:
        help_data = None
        if step_type == InverseStepType.boolean_inverse_exercise:
            help_data = self._get_inverse_concept_help(exercise=exercise)
        elif step_type == InverseStepType.selection_inverse_exercise:
            help_data = self._get_selection_inverse_help()
        elif step_type == InverseStepType.indicate_domain_exercise:
            help_data = self._get_indicate_domain_help(exercise=exercise)
        return help_data

    def _get_inverse_concept_help(self, exercise: FunctionExercise) -> FunctionHelpData:
        identifier = 0
        help_text = 'Para que una gráfica tenga inversa debe de tener...'
        function = exercise.get_main_function()
        x_values, y_values = function.get_points()

        graphs = self._get_constant_graphs(y_values=y_values)
        return FunctionHelpData(identifier=identifier, help_text=help_text, help_expressions=graphs)

    @staticmethod
    def _get_selection_inverse_help() -> FunctionHelpData:
        identifier = 0
        help_text = 'Para que una gráfica tenga inversa debe de tener...'
        constant_graph_help = Function(function_id=-1, expression='x', domain=None, is_main_graphic=False,
                                       inverse_function=None)
        return FunctionHelpData(identifier=identifier, help_text=help_text, help_expressions=[constant_graph_help])

    def _get_indicate_domain_help(self, exercise: FunctionExercise) -> FunctionHelpData:
        identifier = 0
        help_text = 'El dominio es el rango de valores...'
        x_values, y_values = exercise.get_domain_values()
        x_graphs = [
            Function(function_id=-1, expression=f'{constant}', domain=None, is_main_graphic=False,
                     inverse_function=None)
            for constant in x_values[::4]
        ]
        y_graphs = [
            Function(function_id=-1, expression=f'{constant}', domain=None, is_main_graphic=False,
                     inverse_function=None, is_invert=True)
            for constant in y_values[::4]
        ]
        graphs = x_graphs + y_graphs
        return FunctionHelpData(identifier=identifier, help_text=help_text, help_expressions=graphs)

    def _get_constant_graphs(self, y_values):
        unique_elements = set()
        duplicated_element = min(y_values)
        for y_value in y_values:
            if y_value not in unique_elements:
                unique_elements.add(y_value)
            else:
                duplicated_element = y_value
                break
        y_range = min(y_values), max(y_values)
        constant_graphs = self._generate_constant_graphs(y_range=y_range, start_point=duplicated_element)

        graphs = [
            Function(function_id=-1, expression=f'{constant}', domain=None, is_main_graphic=False,
                     inverse_function=None)
            for constant in constant_graphs
        ]
        return graphs

    @staticmethod
    def _generate_constant_graphs(y_range: (tuple, tuple), start_point: int) -> List[int]:
        nums = [num for num in range(int(start_point), int(round(y_range[1])))]
        nums += [num for num in range(int(round(y_range[0])), int(start_point))]
        return nums

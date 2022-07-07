from collections import defaultdict
from typing import List

from ..models.enums.inverse_step_type import InverseStepType
from ..models.function import Function
from ..models.function_exercise import FunctionExercise
from ..models.function_help_data import FunctionHelpData
from ..models.function_point import FunctionPoint


class HelpDataMapper:
    def __init__(self, exercise: FunctionExercise):
        self._exercise = exercise

    def get_help_data(self, step_type: InverseStepType) -> FunctionHelpData:
        help_data = None
        if step_type == InverseStepType.boolean_inverse_exercise:
            help_data = self._get_inverse_concept_help()
        elif step_type == InverseStepType.selection_inverse_exercise:
            help_data = self._get_selection_inverse_help()
        elif step_type == InverseStepType.indicate_domain_exercise:
            help_data = self._get_indicate_domain_help()
        elif step_type == InverseStepType.indicate_range_exercise:
            help_data = self._get_indicate_range_help()
        elif step_type == InverseStepType.indicate_bounded_range_exercise:
            help_data = self._get_indicate_bounded_range_help()
        elif step_type == InverseStepType.maximum_relative_exercise:
            help_data = self._get_maximum_relative_help()
        elif step_type == InverseStepType.maximum_absolute_exercise:
            help_data = self._get_maximum_absolute_help()
        elif step_type == InverseStepType.minimum_relative_exercise:
            help_data = self._get_minimum_relative_help()
        elif step_type == InverseStepType.minimum_absolute_exercise:
            help_data = self._get_minimum_absolute_help()
        return help_data

    def _get_inverse_concept_help(self) -> FunctionHelpData:
        help_text = '¿Tiene imágenes repetidas?'
        function = self._exercise.get_main_function()
        x_values, y_values = function.get_points(small_sample=True)

        graphs, function_points = self._get_constant_graphs(x_values=x_values, y_values=y_values)
        return FunctionHelpData(help_text=help_text, help_expressions=graphs,
                                help_points=function_points)

    @staticmethod
    def _get_selection_inverse_help() -> FunctionHelpData:
        help_text = 'La inversa de una función es su simétrica respecto a la bisectriz de la función y=x.'
        constant_graph_help = Function(function_id=-1, expression='x', domain='[-10, 10]', is_main_graphic=False,
                                       is_elementary_graph=False, inverse_function=None)
        return FunctionHelpData(help_text=help_text, help_expressions=[constant_graph_help])

    def _get_indicate_domain_help(self) -> FunctionHelpData:
        help_text = 'Recuerda que el dominio lo forman los puntos con imagen.'
        x_values, y_values = self._exercise.get_domain_range_values()
        x_values_by_y_value = defaultdict(list)
        y_values_by_x_value = defaultdict(list)
        for x_value, y_value in zip(x_values, y_values):
            x_values_by_y_value[y_value].append(x_value)
            y_values_by_x_value[x_value].append(y_value)

        unique_sorted_x_values = sorted(
            [
                x_value
                for x_value in set(x_values)
                if -5 < x_value < 5 and any(True for y_value in y_values_by_x_value[x_value] if -5 < y_value < 5)
            ]
        )
        unique_sorted_y_values = sorted(
            [
                y_value
                for y_value in set(y_values)
                if -5 < y_value < 5 and any(True for x_value in x_values_by_y_value[y_value] if -5 < x_value < 5)
            ]
        )
        slicing_x_number = len(unique_sorted_x_values) // 10 if len(unique_sorted_x_values) // 10 != 0 else 1
        slicing_y_number = len(unique_sorted_y_values) // 10 if len(unique_sorted_y_values) // 10 != 0 else 1

        graphs = []
        for x_value in unique_sorted_x_values[::slicing_x_number]:
            y_value = min(y_val for y_val in y_values_by_x_value[x_value] if -5 < y_val < 5)
            x_graph = Function(function_id=-1, expression=f'{x_value}', domain=f'[-10, {y_value}]',
                               is_main_graphic=False, is_elementary_graph=False, inverse_function=None, is_invert=True)
            graphs.append(x_graph)
        for y_value in unique_sorted_y_values[::slicing_y_number]:
            x_value = min(x_val for x_val in x_values_by_y_value[y_value] if -5 < x_val < 5)
            x_graph = Function(function_id=-1, expression=f'{y_value}', domain=f'[-10, {x_value}]',
                               is_main_graphic=False, is_elementary_graph=False, inverse_function=None, is_invert=False)
            graphs.append(x_graph)
        return FunctionHelpData(help_text=help_text, help_expressions=graphs)

    def _get_constant_graphs(self, x_values, y_values):
        unique_elements = set()
        duplicated_elements = []
        x_values_by_y_value = defaultdict(list)
        for x_value, y_value in zip(x_values, y_values):
            if y_value not in unique_elements:
                unique_elements.add(y_value)
                x_values_by_y_value[y_value].append(x_value)
            else:
                if -5 < y_value < 5:
                    duplicated_elements.append(y_value)
                    x_values_by_y_value[y_value].append(x_value)

        function_points = []
        if not duplicated_elements:
            y_range = min(y_values), max(y_values)
            graphs = self._generate_constant_graphs(y_range=y_range)
        else:
            duplicated_elements = sorted(duplicated_elements)
            duplicated_element = duplicated_elements[len(duplicated_elements) // 2]
            graphs = [duplicated_element]
            duplicated_x_values = x_values_by_y_value[duplicated_element]
            function_points = [
                FunctionPoint(x_value=duplicated_x, y_value=duplicated_element) for duplicated_x in duplicated_x_values
            ]
        index = -1 if len(graphs) > 1 else 1
        constant_graphs = [
            Function(function_id=-1, expression=f'{constant}', domain='[-10, 10]', is_main_graphic=False,
                     is_elementary_graph=False, inverse_function=None)
            for constant in graphs[:index]
        ]
        return constant_graphs, function_points

    @staticmethod
    def _generate_constant_graphs(y_range: (tuple, tuple)) -> List[int]:
        start_point, end_point = y_range
        nums = [num for num in range(int(start_point), int(round(end_point) + 1))]
        return nums

    @staticmethod
    def _get_indicate_range_help() -> FunctionHelpData:
        help_text = 'Recuerda que el recorrido son las imágenes que alcanza la función.'
        return FunctionHelpData(help_text=help_text, help_expressions=[])

    @staticmethod
    def _get_indicate_bounded_range_help() -> FunctionHelpData:
        help_text = 'Para que una gráfica se diga que está acotada...'
        return FunctionHelpData(help_text=help_text, help_expressions=[])

    @staticmethod
    def _get_maximum_relative_help() -> FunctionHelpData:
        help_text = 'Para que un punto sea máximo relativo tiene que tener...'
        return FunctionHelpData(help_text=help_text, help_expressions=[])

    @staticmethod
    def _get_maximum_absolute_help() -> FunctionHelpData:
        help_text = 'Para que un punto sea máximo absoluto tiene que tener...'
        return FunctionHelpData(help_text=help_text, help_expressions=[])

    @staticmethod
    def _get_minimum_relative_help() -> FunctionHelpData:
        help_text = 'Para que un punto sea mínimo relativo tiene que tener...'
        return FunctionHelpData(help_text=help_text, help_expressions=[])

    @staticmethod
    def _get_minimum_absolute_help() -> FunctionHelpData:
        help_text = 'Para que un punto sea mínimo absoluto tiene que tener...'
        return FunctionHelpData(help_text=help_text, help_expressions=[])

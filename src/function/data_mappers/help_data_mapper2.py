from collections import defaultdict
from typing import List

from ..models.enums.step_type import StepType
from ..models.function import Function
from ..models.function_exercise import FunctionExercise
from ..models.help_data import HelpData
from ..models.point import Point


class HelpDataMapper:
    def __init__(self, exercise: FunctionExercise):
        self._exercise = exercise

    def get_help_data(self, step_type: StepType) -> List[HelpData]:
        help_data = None
        if step_type == StepType.boolean_inverse_exercise:
            help_data = self._get_inverse_concept_help()
        elif step_type == StepType.selection_inverse_exercise:
            help_data = self._get_selection_inverse_help()
        elif step_type == StepType.indicate_domain_exercise:
            help_data = self._get_indicate_domain_help()
        elif step_type == StepType.indicate_range_exercise:
            help_data = self._get_indicate_range_help()
        elif step_type == StepType.indicate_bounded_range_exercise:
            help_data = self._get_indicate_bounded_range_help()
        elif step_type == StepType.indicate_roots_exercise:
            help_data = self._get_indicate_indicate_roots_help()
        elif step_type == StepType.maximum_relative_exercise:
            help_data = self._get_maximum_relative_help()
        elif step_type == StepType.maximum_absolute_exercise:
            help_data = self._get_maximum_absolute_help()
        elif step_type == StepType.minimum_relative_exercise:
            help_data = self._get_minimum_relative_help()
        elif step_type == StepType.minimum_absolute_exercise:
            help_data = self._get_minimum_absolute_help()
        return help_data

    def _get_inverse_concept_help(self) -> List[FunctionHelpData]:
        help_text = 'En la gráfica siguiente se puede observar como las constantes no cortan la gráfica en dos puntos.' \
                    ' Indicando que no tiene imágenes repetidas.'
        main_function = Function(function_id=1000, expression='x**3', domain='(2, 2)', is_main_graphic=True,
                                 is_invert=False)
        support_functions, support_points = self._get_constant_functions(x_values=main_function.x_values,
                                                                         y_values=main_function.y_values)
        first_help_data = FunctionHelpData(texts=[help_text], functions=[main_function, *support_functions],
                                           points=support_points, order=0)

        help_text = 'En la gráfica siguiente se puede observar como las constantes cortan la gráfica en dos puntos.' \
                    ' Indicando que tiene imágenes repetidas.'
        main_function = Function(function_id=1000, expression='x**2', domain='(2, 2)', is_main_graphic=True,
                                 is_invert=False)
        support_functions, support_points = self._get_constant_functions(x_values=main_function.x_values,
                                                                         y_values=main_function.y_values)
        second_help_data = FunctionHelpData(texts=[help_text], functions=[main_function, *support_functions],
                                            points=support_points, order=0)
        return [first_help_data, second_help_data]

    @staticmethod
    def _get_selection_inverse_help() -> FunctionHelpData:
        help_text = 'La inversa de una función es su simétrica respecto a la bisectriz de la función y=x.'
        constant_graph_help = Function(function_id=-1, expression='x', domain='[-10, 10]', is_main_graphic=False,
                                       is_elementary_graph=False, inverse_function=None)
        return FunctionHelpData(help_text=help_text, help_expressions=[constant_graph_help])

    def _get_indicate_domain_help(self) -> FunctionHelpData:
        help_text = 'Recuerda que el dominio lo forman los puntos con imagen.'
        return FunctionHelpData(help_text=help_text, help_expressions=[])

    def _get_constant_functions(self, x_values, y_values):
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
        help_text = '¿El conjunto imagen de la función está acotado?'
        return FunctionHelpData(help_text=help_text, help_expressions=[])

    @staticmethod
    def _get_indicate_indicate_roots_help() -> FunctionHelpData:
        help_text = 'Observa los cortes de la función con el eje de las abscisas.'
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

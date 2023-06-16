from typing import List

from ..models import HelpStep, Function, FunctionExercise, HelpData
from ..models.enums.step_type import StepType


class HelpDataMapper:
    def __init__(self, exercise: FunctionExercise):
        self._exercise = exercise

    def get_help_data(self, step_type: StepType) -> List[HelpData]:
        help_data_list = []
        if step_type == StepType.inverse_concept_exercise:
            help_data_list = self._get_inverse_concept_help()
        # elif step_type == StepType.selection_inverse_exercise:
        #     help_data_list = self._get_selection_inverse_help()
        # elif step_type == StepType.delimited_inverse_exercise:
        #     help_data_list = self._get_delimited_inverse_help()
        #
        # elif step_type == StepType.maximum_relative_exercise:
        #     help_data_list = self._get_maximum_relative_help()
        # elif step_type == StepType.maximum_absolute_exercise:
        #     help_data_list = self._get_maximum_absolute_help()
        # elif step_type == StepType.minimum_relative_exercise:
        #     help_data_list = self._get_minimum_relative_help()
        # elif step_type == StepType.minimum_absolute_exercise:
        #     help_data_list = self._get_minimum_absolute_help()

        elif step_type == StepType.indicate_domain_exercise:
            help_data_list = self._get_indicate_domain_help()
        elif step_type == StepType.indicate_range_exercise:
            help_data_list = self._get_indicate_range_help()
        elif step_type == StepType.indicate_elementary_shift_exercise:
            help_data_list = self._get_indicate_elementary_shift_exercise_help()
        return help_data_list

    def _get_indicate_elementary_shift_exercise_help(self):
        first_help_data = self._get_first_help_data_elementary_shift()
        second_help_data = self._get_second_help_data_elementary_shift()
        return [first_help_data, second_help_data]

    def _get_first_help_data_elementary_shift(self) -> HelpData:
        first_step = self._get_first_step_elementary_shift()
        second_step = self._get_second_step_elementary_shift()
        function = Function(function_id=0, expression='(x)**2', domain=(-3, 3), is_main_graphic=True)
        return HelpData(order=0, function=function, help_steps=[first_step, second_step], text='Super cool text')

    def _get_first_step_elementary_shift(self) -> HelpStep:
        function = Function(function_id=0, expression='(x + 1)**2', domain=(-3, 3), is_main_graphic=False)
        return HelpStep(order=0, functions=[function], text='El desplazamiento hacía la izquierda',
                        function_color='blue')

    def _get_second_step_elementary_shift(self) -> HelpStep:
        function = Function(function_id=0, expression='(x - 1)**2', domain=(-3, 3), is_main_graphic=False)
        return HelpStep(order=1, functions=[function], text='El desplazamiento hacía la derecha',
                        function_color='purple')

    def _get_second_help_data_elementary_shift(self) -> HelpData:
        first_step = self._get_third_step_elementary_shift()
        second_step = self._get_fourth_step_elementary_shift()
        function = Function(function_id=0, expression='(x)**2', domain=(-3, 3), is_main_graphic=True)
        return HelpData(order=1, function=function, help_steps=[first_step, second_step], text='Super cool text x2')

    def _get_third_step_elementary_shift(self) -> HelpStep:
        function = Function(function_id=0, expression='(x)**2 + 1', domain=(-3, 3), is_main_graphic=False)
        return HelpStep(order=0, functions=[function], text='El desplazamiento hacía arriba', function_color='blue')

    def _get_fourth_step_elementary_shift(self) -> HelpStep:
        function = Function(function_id=0, expression='(x)**2 - 1', domain=(-3, 3), is_main_graphic=False)
        return HelpStep(order=1, functions=[function], text='El desplazamiento hacía abajo', function_color='purple')

    def _get_inverse_concept_help(self):
        return None

    def _get_selection_inverse_help(self):
        return None

    def _get_delimited_inverse_help(self):
        return None

    def _get_indicate_domain_help(self):
        first_help_data = self._get_first_help_data_domain()
        return [first_help_data]

    def _get_first_help_data_domain(self) -> HelpData:
        function_one = Function(function_id=0, expression='(x)**2', x_values_range=(0, 2), is_main_graphic=True,
                                domain='[0, 2)')
        function_one.setup_data((-5, 5))
        function_two = Function(function_id=0, expression='x', x_values_range=(3, 5), is_main_graphic=True,
                                domain='(3, +inf)')
        function_two.setup_data((-5, 5))
        help_step_one = self._get_first_help_step_domain()
        help_step_two = self._get_second_help_step_domain()
        return HelpData(order=0, title='Apuntes sobre el dominio de una función',
                        functions=[function_one, function_two], help_steps=[help_step_one, help_step_two],
                        text='El dominio de una función son todos los valores que toma x para la función. '
                             'En este caso el dominio de la función es "[0, 2) U (3, +inf)"')

    def _get_first_help_step_domain(self) -> HelpStep:
        function_one = Function(function_id=0, expression='0', x_values_range=(-5, 5), is_main_graphic=False,
                                domain='(-inf, +inf)', is_invert_function=True)
        function_one.setup_data((-5, 5))

        function_two = Function(function_id=0, expression='1', x_values_range=(-5, 5), is_main_graphic=False,
                                domain='(-inf, +inf)', is_invert_function=True)
        function_two.setup_data((-5, 5))

        function_three = Function(function_id=0, expression='4', x_values_range=(-5, 5), is_main_graphic=False,
                                  domain='(-inf, +inf)', is_invert_function=True)
        function_three.setup_data((-5, 5))

        text = 'Para la función dada, los puntos siguientes sí están definidos en el dominio porque las cotas son. '
        return HelpStep(order=0, functions=[function_one, function_two, function_three], text=text,
                        function_color='blue')

    def _get_second_help_step_domain(self) -> HelpStep:
        function_one = Function(function_id=0, expression='2', x_values_range=(-5, 5), is_main_graphic=False,
                                domain='(-inf, +inf)', is_invert_function=True)
        function_one.setup_data((-5, 5))

        function_two = Function(function_id=0, expression='3', x_values_range=(-5, 5), is_main_graphic=False,
                                domain='(-inf, +inf)', is_invert_function=True)
        function_two.setup_data((-5, 5))

        function_three = Function(function_id=0, expression='2.5', x_values_range=(-5, 5), is_main_graphic=False,
                                  domain='(-inf, +inf)', is_invert_function=True)
        function_three.setup_data((-5, 5))

        text = 'Para la función dada los puntos siguientes no están definidos en el dominio porque las cotas son. '
        return HelpStep(order=0, functions=[function_one, function_two, function_three], text=text,
                        function_color='red')

    def _get_indicate_range_help(self):
        first_help_data = self._get_first_help_data_range()
        return [first_help_data]

    def _get_first_help_data_range(self) -> HelpData:
        function_one = Function(function_id=0, expression='(x)**2', x_values_range=(0, 2), is_main_graphic=True,
                                domain='[0, 2)')
        function_one.setup_data((-5, 5))
        function_two = Function(function_id=0, expression='x + 0.5', x_values_range=(4, 5), is_main_graphic=True,
                                domain='[4, +inf)')
        function_two.setup_data((-5, 5))
        help_step_one = self._get_first_help_step_range()
        help_step_two = self._get_second_help_step_range()
        return HelpData(order=0, title='Apuntes sobre el rango de una función',
                        functions=[function_one, function_two], help_steps=[help_step_one, help_step_two],
                        text='El rango de una función son todos los valores que toma y para la función. '
                             'En este caso el rango de la función es "[0, 4) U [4.5, +inf)"')

    def _get_first_help_step_range(self) -> HelpStep:
        function_one = Function(function_id=0, expression='0', x_values_range=(-5, 5), is_main_graphic=False,
                                domain='(-inf, +inf)')
        function_one.setup_data((-5, 5))

        function_two = Function(function_id=0, expression='4.5', x_values_range=(-5, 5), is_main_graphic=False,
                                domain='(-inf, +inf)')
        function_two.setup_data((-5, 5))

        function_three = Function(function_id=0, expression='5', x_values_range=(-5, 5), is_main_graphic=False,
                                  domain='(-inf, +inf)')
        function_three.setup_data((-5, 5))

        text = 'Para la función dada, los puntos siguientes sí están definidos en el rango porque las cotas son. '
        return HelpStep(order=0, functions=[function_one, function_two, function_three], text=text,
                        function_color='blue')

    def _get_second_help_step_range(self) -> HelpStep:
        function_one = Function(function_id=0, expression='4', x_values_range=(-5, 5), is_main_graphic=False,
                                domain='(-inf, +inf)')
        function_one.setup_data((-5, 5))

        function_two = Function(function_id=0, expression='4.25', x_values_range=(-5, 5), is_main_graphic=False,
                                domain='(-inf, +inf)')
        function_two.setup_data((-5, 5))

        text = 'Para la función dada los puntos siguientes no están definidos en el rango porque las cotas son. '
        return HelpStep(order=0, functions=[function_one, function_two], text=text,
                        function_color='red')

        ########################################

    def _get_indicate_bounded_range_help(self):
        pass

    def _get_indicate_indicate_roots_help(self):
        pass

    def _get_maximum_relative_help(self):
        pass

    def _get_maximum_absolute_help(self):
        pass

    def _get_minimum_relative_help(self):
        pass

    def _get_minimum_absolute_help(self):
        pass

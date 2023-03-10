from typing import List

from ..models import HelpStep, Function, FunctionExercise, HelpData
from ..models.enums.step_type import StepType


class HelpDataMapper:
    def __init__(self, exercise: FunctionExercise):
        self._exercise = exercise

    def get_help_data(self, step_type: StepType) -> List[HelpData]:
        help_data_list = []
        if step_type == StepType.boolean_inverse_exercise:
            help_data_list = self._get_inverse_concept_help()
        elif step_type == StepType.selection_inverse_exercise:
            help_data_list = self._get_selection_inverse_help()
        elif step_type == StepType.indicate_domain_exercise:
            help_data_list = self._get_indicate_domain_help()
        elif step_type == StepType.indicate_range_exercise:
            help_data_list = self._get_indicate_range_help()
        elif step_type == StepType.indicate_bounded_range_exercise:
            help_data_list = self._get_indicate_bounded_range_help()
        elif step_type == StepType.indicate_roots_exercise:
            help_data_list = self._get_indicate_indicate_roots_help()
        elif step_type == StepType.maximum_relative_exercise:
            help_data_list = self._get_maximum_relative_help()
        elif step_type == StepType.maximum_absolute_exercise:
            help_data_list = self._get_maximum_absolute_help()
        elif step_type == StepType.minimum_relative_exercise:
            help_data_list = self._get_minimum_relative_help()
        elif step_type == StepType.minimum_absolute_exercise:
            help_data_list = self._get_minimum_absolute_help()
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

    ########################################

    def _get_inverse_concept_help(self):
        pass

    def _get_selection_inverse_help(self):
        pass

    def _get_indicate_domain_help(self):
        pass

    def _get_indicate_range_help(self):
        pass

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

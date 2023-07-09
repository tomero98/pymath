from PyQt5.QtCore import pyqtSignal

from . import DomainDefinitionComponent
from ...models import FunctionExercise, FunctionStep, ExerciseResume


class RangeDefinitionComponent(DomainDefinitionComponent):
    continue_signal = pyqtSignal(bool)
    label = 'Indicar el rango de la función'
    _ORIENTATION = 'horizontal'

    def __init__(self, exercise: FunctionExercise, step: FunctionStep, resume: ExerciseResume,
                 need_help_data: bool = False):
        super(RangeDefinitionComponent, self).__init__(
            exercise=exercise, step=step, resume=resume, need_help_data=need_help_data
        )

    def _set_validation(self, *args, **kwargs):
        return self._exercise.validate_range_expression(*args, **kwargs)

    def _is_exercise_correct(self, expression_selected: str) -> bool:
        is_correct, _, _ = self._exercise.validate_range_expression(user_range_input=expression_selected)
        return is_correct

    def _get_correct_expression(self) -> str:
        return self._exercise.get_range_expression()

    def _get_error_label_text(self, correct_response: str) -> str:
        return f'Incorrecto. El rango de la función es el siguiente: {correct_response}'

    def _show_input(self, input_to_show: str):
        if self._linear_region_items:
            for linear_region_item in self._linear_region_items:
                self._plot_widget.removeItem(linear_region_item)

        input_parts = input_to_show.split(' U ')
        for input_part in input_parts:
            limits = input_part[1:-1].split(',')
            force_include_upper_limit = False
            force_include_lower_limit = False
            if input_part[0] == '(' and '-inf' not in input_part:
                first_condition = f'{limits[0].replace(" ", "")}]' in input_to_show
                second_condition = f'[{limits[0].replace(" ", "")}' in input_to_show
                force_include_lower_limit = first_condition or second_condition
            if input_part[-1] == ')' and '+inf' not in input_part:
                first_condition = f'[{limits[-1].replace(" ", "")}' in input_to_show
                second_condition = f'{limits[-1].replace(" ", "")}]' in input_to_show
                force_include_upper_limit = first_condition or second_condition
            self._add_range_selection_dialog(
                range_added=input_part, force_include_upper_limit=force_include_upper_limit,
                force_include_lower_limit=force_include_lower_limit
            )

        for region_item in self._linear_region_items:
            region_item.setMovable(False)

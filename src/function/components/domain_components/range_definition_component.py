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
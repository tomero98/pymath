from ..option_selection_component import OptionSelectionComponent
from ...models import ExerciseResume, FunctionExercise, FunctionStep


class InverseConceptComponent(OptionSelectionComponent):
    label = 'Indicar si existe inversa: '

    def __init__(self, exercise: FunctionExercise, step: FunctionStep, resume: ExerciseResume, need_help_data: bool):
        super(InverseConceptComponent, self).__init__(exercise=exercise, step=step, resume=resume,
                                                      need_help_data=need_help_data)

    def _get_options_to_display(self):
        return ['SÍ', 'NO']

    def _get_function_to_draw(self):
        return self._exercise.get_main_function()

    def _get_correct_expression(self):
        return 'SÍ' if self._exercise.has_main_function_inverse() else 'NO'

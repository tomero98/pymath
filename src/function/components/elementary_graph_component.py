from .selection_component import SelectionComponent
from ..models.exercise_resume import ExerciseResume
from ..models.function_exercise import FunctionExercise
from ..models.function_step import FunctionStep


class ElementaryGraphComponent(SelectionComponent):
    label = 'Seleccionar la función.'

    def __init__(self, exercise: FunctionExercise, step: FunctionStep, resume: ExerciseResume):
        super(ElementaryGraphComponent, self).__init__(exercise=exercise, step=step, resume=resume)

    def _get_functions_to_display_as_options(self):
        return self._exercise.functions

    def _get_function_to_draw(self):
        return self._exercise.get_main_function()

    def _get_correct_expression(self):
        return self._exercise.get_main_function().get_math_expression()

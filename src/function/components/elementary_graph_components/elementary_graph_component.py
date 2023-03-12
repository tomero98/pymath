from ..selection_component import SelectionComponent
from ...models import ExerciseResume, FunctionExercise, FunctionStep, Function


class ElementaryGraphComponent(SelectionComponent):
    label = 'Seleccionar la función.'

    def __init__(self, exercise: FunctionExercise, step: FunctionStep, resume: ExerciseResume):
        super(ElementaryGraphComponent, self).__init__(exercise=exercise, step=step, resume=resume)

    def _get_options_to_display(self):
        return [function.get_math_expression() for function in self._exercise.functions]

    def _get_function_to_draw(self):
        return self._exercise.get_main_function()

    def _get_correct_expression(self):
        return self._exercise.get_main_function().get_math_expression()

    def _get_error_function(self, expression: str) -> Function:
        return next(function for function in self._exercise.functions if function.get_math_expression() == expression)

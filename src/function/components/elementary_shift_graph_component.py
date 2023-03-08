import random

from PyQt5.QtCore import pyqtSignal

from .selection_component import SelectionComponent
from ..models.exercise_resume import ExerciseResume
from ..models.function import Function
from ..models.function_exercise import FunctionExercise
from ..models.function_step import FunctionStep


class ElementaryShiftGraphComponent(SelectionComponent):
    continue_signal = pyqtSignal(ExerciseResume)
    back_signal = pyqtSignal(ExerciseResume)
    resume_signal = pyqtSignal(ExerciseResume)

    label = 'Seleccionar la función.'

    def __init__(self, exercise: FunctionExercise, step: FunctionStep, resume: ExerciseResume):
        self._main_function = None

        super(ElementaryShiftGraphComponent, self).__init__(exercise=exercise, step=step, resume=resume)

    def _setup_data(self):
        self._setup_functions()

    def _setup_functions(self):
        functions = []
        main_function = self._exercise.get_main_function()
        main_function_expression = main_function.expression

        expression = f'{main_function_expression} - 1'
        function = Function(function_id=0, expression=expression, domain=main_function.domain, is_main_graphic=False)
        functions.append(function)

        expression = f'{main_function_expression} + 1'
        function = Function(function_id=0, expression=expression, domain=main_function.domain, is_main_graphic=False)
        functions.append(function)

        expression_to_replace = 'x - 1' if '(x)' in main_function_expression else '(x - 1)'
        expression = main_function_expression.replace('x', expression_to_replace)
        function = Function(function_id=0, expression=expression, domain=main_function.domain, is_main_graphic=False)
        functions.append(function)

        expression_to_replace = 'x + 1' if '(x)' in main_function_expression else '(x + 1)'
        expression = main_function_expression.replace('x', expression_to_replace)
        function = Function(function_id=0, expression=expression, domain=main_function.domain, is_main_graphic=False)
        functions.append(function)

        index = random.randint(0, 3)
        self._main_function = functions[index]
        self._main_function.is_main_graphic = True
        self._functions = functions

    def _get_functions_to_display_as_options(self):
        return self._functions

    def _get_function_to_draw(self):
        return self._main_function

    def _get_correct_expression(self):
        return self._main_function.get_math_expression()

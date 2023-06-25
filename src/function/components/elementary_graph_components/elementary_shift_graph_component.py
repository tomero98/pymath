import random
from typing import List

import pyqtgraph

from .elementary_graph_component import ElementaryGraphComponent
from ...factories import PlotFactory2
from ...models import FunctionExercise, FunctionStep, ExerciseResume, Function
from ...models.enums import ResumeState


class ElementaryShiftGraphComponent(ElementaryGraphComponent):
    label = 'Seleccionar el desplazamiento.'

    def __init__(self, exercise: FunctionExercise, step: FunctionStep, resume: ExerciseResume, need_help_data: bool):
        self._main_function = None

        self._functions: List[Function] = []

        super(ElementaryShiftGraphComponent, self).__init__(exercise=exercise, step=step, resume=resume,
                                                            need_help_data=need_help_data)

    def _setup_data(self):
        self._setup_functions()

    def _setup_functions(self):
        functions = []
        main_function = self._exercise.get_main_function()[0]
        main_function_expression = main_function.expression

        expression = f'{main_function_expression} - 1'
        function = Function(function_id=1, expression=expression, domain=main_function.domain, is_main_graphic=False,
                            x_values_range=(-5, 5))
        functions.append(function)

        expression = f'{main_function_expression} + 1'
        function = Function(function_id=2, expression=expression, domain=main_function.domain, is_main_graphic=False,
                            x_values_range=(-5, 5))
        functions.append(function)

        expression_to_replace = 'x - 1' if '(x)' in main_function_expression else '(x - 1)'
        expression = main_function_expression.replace('x', expression_to_replace)
        function = Function(function_id=3, expression=expression, domain=main_function.domain, is_main_graphic=False,
                            x_values_range=(-5, 5))
        functions.append(function)

        expression_to_replace = 'x + 1' if '(x)' in main_function_expression else '(x + 1)'
        expression = main_function_expression.replace('x', expression_to_replace)
        function = Function(function_id=4, expression=expression, domain=main_function.domain, is_main_graphic=False,
                            x_values_range=(-5, 5))
        functions.append(function)

        if not self._resume:
            main_function = self._select_main_function_random(functions=functions)
        else:
            main_function = self._select_main_function_using_resume(functions=functions)
        self._main_function = main_function
        self._main_function.setup_data(plot_range=(-5, 5))
        self._main_function.is_main_graphic = True
        self._functions = functions

    def _select_main_function_random(self, functions: List[Function]) -> Function:
        index = random.randint(0, 3)
        return functions[index]

    def _select_main_function_using_resume(self, functions: List[Function]) -> Function:
        return next(
            function for function in functions if function.function_id == self._resume.function_id
        )

    def _get_plot_widget(self) -> pyqtgraph.PlotWidget:
        plot_widget = PlotFactory2.get_plot(function_range=self._exercise.plot_range)
        PlotFactory2.set_functions(graph=plot_widget, functions=[self._main_function], function_width=1, color='white',
                                   show_limits=self._show_main_function_limits)
        return plot_widget

    def _get_options_to_display(self):
        return [function.get_math_expression() for function in self._functions]

    def _get_function_to_draw(self):
        return self._main_function

    def _get_correct_expression(self):
        return self._main_function.get_math_expression()

    def _get_error_function(self, expression: str) -> Function:
        return next(function for function in self._functions if function.get_math_expression() == expression)

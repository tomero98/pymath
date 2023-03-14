import random

from PyQt5.QtCore import pyqtSignal

from ..graph_interaction_component import GraphInteractionComponent
from ...factories import PlotFactory2
from ...models import FunctionExercise, FunctionStep, ExerciseResume, Function


class InverseSelectionComponent(GraphInteractionComponent):
    continue_signal = pyqtSignal(bool)
    label = 'Seleccionar la inversa'

    def __init__(self, exercise: FunctionExercise, step: FunctionStep, resume: ExerciseResume,
                 need_help_data: bool = False):
        super(InverseSelectionComponent, self).__init__(
            exercise=exercise, step=step, resume=resume, need_help_data=need_help_data,
        )

    def _on_click_validation_button(self):
        pass

    def _get_correct_expression(self):
        return 'inverse'

    def _get_function_to_draw(self):
        return self._exercise.get_main_function()

    def _is_exercise_correct(self, expression_selected):
        correct_expression = self._get_correct_expression()
        return expression_selected == correct_expression

    def _set_plot_widget(self):
        super(InverseSelectionComponent, self)._set_plot_widget()
        main_function = self._exercise.get_main_function()
        functions = self._get_option_function()
        colors = [(255, 0, 255), (255, 0, 0), (0, 0, 255)]
        random.shuffle(colors)
        PlotFactory2.set_functions(graph=self._plot_widget, functions=[functions[0]], function_width=3,
                                   click_function=self._on_graph_click, color=colors.pop())
        PlotFactory2.set_functions(graph=self._plot_widget, functions=[functions[1]], function_width=3,
                                   click_function=self._on_graph_click, color=colors.pop())
        PlotFactory2.set_graph_using_points(
            graph=self._plot_widget, x_values=main_function.y_values, y_values=main_function.x_values, function_width=3,
            click_function=self._on_graph_click, color=colors.pop(), function_name='inverse'
        )

    def _get_option_function(self):
        return [function for function in self._exercise.functions if not function.is_main_graphic]

    def _on_graph_click(self, plot_curve_item_selected):
        self._validate_exercise(expression_selected=plot_curve_item_selected.metaData['name'])

    def _validate_exercise(self, expression_selected: str, is_resume: bool = False):
        super()._validate_exercise(expression_selected=expression_selected, is_resume=is_resume)
        correct_expression = self._get_correct_expression()
        is_answer_correct = expression_selected == correct_expression
        if not is_answer_correct:
            function = next(
                function for function in self._exercise.functions if function.expression == expression_selected)
        else:
            function = None
        self._set_graph(function=function, is_answer_correct=is_answer_correct)

    def _set_graph(self, function: Function, is_answer_correct: bool):
        border_color = '#2F8C53' if is_answer_correct else 'red'
        if not is_answer_correct:
            self._help_text.setText('Incorrecto.')
            self._update_plot_with_error_data(function=function)
        else:
            self._help_text.setText('Correcto.')
        self._help_text.setVisible(True)
        self._help_text.setStyleSheet(f'color: {border_color}')

        self._continue_button.setStyleSheet(f'background: {border_color}')
        self._continue_button.setDisabled(False)

        if self._exercise.exercise_order != 0 or self._step.order != 0:
            self._back_button.setDisabled(False)

    def _update_plot_with_error_data(self, function: Function):
        PlotFactory2.reset_graph(self._plot_widget)

        main_function = self._exercise.get_main_function()
        PlotFactory2.set_functions(graph=self._plot_widget, functions=[main_function], function_width=5, color='white')
        PlotFactory2.set_functions(graph=self._plot_widget, functions=[function], function_width=3, color='red')
        PlotFactory2.set_graph_using_points(graph=self._plot_widget, x_values=main_function.y_values,
                                            y_values=main_function.x_values, function_width=3, color='green')

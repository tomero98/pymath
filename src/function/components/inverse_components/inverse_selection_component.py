import random

import pyqtgraph
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout

from ..click_selection_component import ClickSelectionComponent
from ...factories import PlotFactory2
from ...models import FunctionExercise, FunctionStep, ExerciseResume


class InverseSelectionComponent(ClickSelectionComponent):
    continue_signal = pyqtSignal(bool)
    label = 'Seleccionar la inversa'

    def __init__(self, exercise: FunctionExercise, step: FunctionStep, resume: ExerciseResume,
                 need_help_data: bool = False):
        super(InverseSelectionComponent, self).__init__(
            exercise=exercise, step=step, resume=resume, need_help_data=need_help_data,
        )

        self._function_points_by_expression = {}

        self._plot_widget: pyqtgraph.PlotWidget = None  # noqa
        self._help_text: QLabel = None  # noqa

        self._layout: QVBoxLayout = None  # noqa
        self._bottom_buttons_layout: QHBoxLayout = None  # noqa

    def _get_correct_expression(self):
        return 'inverse'

    def _get_function_to_draw(self):
        return self._exercise.get_main_function()

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

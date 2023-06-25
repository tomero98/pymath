import random

import pyqtgraph
from PyQt5.QtCore import pyqtSignal, Qt

from ..domain_components.graph_interaction_validation_component import GraphInteractionValidationComponent
from ...factories import PlotFactory2
from ...models import FunctionExercise, FunctionStep, ExerciseResume, Function


class InverseSelectionComponent(GraphInteractionValidationComponent):
    continue_signal = pyqtSignal(bool)
    label = 'Seleccionar la inversa'

    def __init__(self, exercise: FunctionExercise, step: FunctionStep, resume: ExerciseResume,
                 need_help_data: bool = False, show_main_function_limits: bool = False):
        super(InverseSelectionComponent, self).__init__(
            exercise=exercise, step=step, resume=resume, need_help_data=need_help_data,
            show_function_labels=show_main_function_limits
        )
        self._resolved = False

    def _setup_data(self):
        main_function = self._exercise.get_main_function()[0]
        main_function.setup_data(plot_range=self._exercise.plot_range)

    def _setup_layout(self):
        self._layout.addWidget(self._question_label, alignment=Qt.AlignHCenter)
        self._layout.addSpacing(10)
        self._layout.addWidget(self._plot_widget_container, alignment=Qt.AlignTop | Qt.AlignHCenter)
        self._layout.addSpacing(20)
        self._layout.addWidget(self._result_label, alignment=Qt.AlignHCenter)
        self._layout.addStretch()

    def _on_function_to_draw_click(self, plot_curve_item_selected, point_selected):
        pass

    def _on_click_validation_button(self):
        pass

    def _get_correct_expression(self):
        return 'inverse'

    def _is_exercise_correct(self, expression_selected):
        correct_expression = self._get_correct_expression()
        return expression_selected == correct_expression

    def _get_function_to_draw(self):
        return self._exercise.get_main_function()[0]

    def _get_plot_widget(self) -> pyqtgraph.PlotWidget:
        plot_widget = super(InverseSelectionComponent, self)._get_plot_widget()
        main_function = self._exercise.get_main_function()[0]
        functions = self._get_option_function()
        functions[0].setup_data(plot_range=self._exercise.plot_range)
        functions[1].setup_data(plot_range=self._exercise.plot_range)
        colors = [(255, 0, 255), (255, 0, 0), (0, 0, 255)]
        random.shuffle(colors)
        PlotFactory2.set_functions(graph=plot_widget, functions=[functions[0]], function_width=3,
                                   click_function=self._on_graph_click, color=colors.pop())
        PlotFactory2.set_functions(graph=plot_widget, functions=[functions[1]], function_width=3,
                                   click_function=self._on_graph_click, color=colors.pop())
        inverse_color = colors.pop()
        self._setup_inverse_plot(color=inverse_color, function=main_function, plot_widget=plot_widget)

        return plot_widget

    def _setup_inverse_plot(self, color: [str, tuple], function: Function, plot_widget: pyqtgraph.PlotWidget):
        for x_group, y_group in zip(function.y_values, function.x_values):
            PlotFactory2.set_graph_using_points(
                graph=plot_widget, x_values=x_group, y_values=y_group, function_width=3,
                click_function=self._on_graph_click, color=color, function_name='inverse'
            )

    def _get_option_function(self):
        return [function for function in self._exercise.functions if not function.is_main_graphic]

    def _on_graph_click(self, plot_curve_item_selected):
        if not self._resolved:
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

        PlotFactory2.reset_graph(self._plot_widget)
        main_function = self._exercise.get_main_function()[0]
        PlotFactory2.set_functions(graph=self._plot_widget, functions=[main_function], function_width=5, color='white')
        self._setup_inverse_plot(color='green', function=main_function, plot_widget=self._plot_widget)

        self._resolved = True

        if is_answer_correct:
            self._setup_correct_response()
        else:
            self._setup_wrong_response(function=function)
        self._setup_finished_exercise()

    def _setup_correct_response(self, *args, **kwargs):
        self._result_label.setText('Correcto.')
        self._result_label.setStyleSheet('color: green;')
        self._result_label.setVisible(True)

    def _setup_wrong_response(self, function: Function, *args, **kwargs):
        self._result_label.setText('Incorrecto.')
        self._result_label.setStyleSheet('color: red;')
        self._result_label.setVisible(True)
        self._update_plot_with_error_data(function=function)

    def _setup_finished_exercise(self, *args, **kwargs):
        super(InverseSelectionComponent, self)._setup_finished_exercise()

    def _update_plot_with_error_data(self, function: Function):
        PlotFactory2.set_functions(graph=self._plot_widget, functions=[function], function_width=3, color='red')
        help_function_values = [self._exercise.plot_range[0], self._exercise.plot_range[-1]]
        PlotFactory2.set_graph_using_points(graph=self._plot_widget, x_values=help_function_values,
                                            y_values=help_function_values, function_width=1, color='blue')

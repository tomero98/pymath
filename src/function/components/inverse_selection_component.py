import math

import pyqtgraph
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QApplication

from ..factories import PlotFactory
from ..models.function_exercise import FunctionExercise
from ..models.function_step import FunctionStep
from ...projectConf.factories import LabelFactory, ButtonFactory
from ...projectConf.factories.icon_factory import IconFactory
from ...projectConf.models.enums.text_type import TextType


class InverseSelectionComponent(QWidget):
    continue_signal = pyqtSignal(bool)
    validate_signal = pyqtSignal()

    def __init__(self, exercise: FunctionExercise, step: FunctionStep):
        super(InverseSelectionComponent, self).__init__()
        self._exercise = exercise
        self._step = step
        self._is_answer_correct = None
        self._function_points_by_expression = {}

        self._plot_widget: pyqtgraph.PlotWidget = None  # noqa
        self._help_subtitle_widget: QLabel = None  # noqa
        self._ok_button: QPushButton = None  # noqa
        self._fail_button: QPushButton = None  # noqa
        self._help_text: QLabel = None  # noqa

        self._layout: QVBoxLayout = None  # noqa
        self._main_window_layout: QHBoxLayout = None  # noqa
        self._bottom_buttons_layout: QHBoxLayout = None  # noqa

        self._preload_data()
        self._draw()

    def _preload_data(self):
        for function in self._exercise.functions:
            if function.is_main_graphic and function.inverse_function:
                self._function_points_by_expression[
                    function.inverse_function.expression] = function.inverse_function.get_points_range()
            else:
                self._function_points_by_expression[function.expression] = function.get_points_range()

    def _draw(self):
        self._layout = QVBoxLayout()
        question_widget = LabelFactory.get_label_component(text=self._step.question, label_type=TextType.SUBTITLE,
                                                           need_word_wrap=True)
        self._main_window_layout = self._get_main_window_layout()
        self._help_text = LabelFactory.get_label_component(text='', label_type=TextType.NORMAL_TEXT,
                                                           need_word_wrap=True)
        icon = IconFactory.get_icon_widget(image_name='continue_button.png')
        self._continue_button = ButtonFactory.get_button_component(
            title='', function_to_connect=lambda: self._send_continue_signal(), icon=icon, icon_size=40,
            tooltip='Continuar', is_disable=True
        )
        self._layout.addWidget(question_widget, alignment=Qt.AlignHCenter)
        self._layout.addLayout(self._main_window_layout)
        self._layout.addWidget(self._help_text, alignment=Qt.AlignHCenter)
        self._layout.addWidget(self._continue_button, alignment=Qt.AlignLeft)
        self.setLayout(self._layout)

    def _get_main_window_layout(self) -> QHBoxLayout:
        main_window_layout = QHBoxLayout()

        inverse_function = self._exercise.get_inverse_graph()
        self._plot_widget = PlotFactory.get_plot([*self._exercise.functions, inverse_function])

        main_window_layout.addStretch()
        main_window_layout.addWidget(self._plot_widget, alignment=Qt.AlignHCenter)
        main_window_layout.addStretch()
        self.proxy = pyqtgraph.SignalProxy(self._plot_widget.scene().sigMouseMoved, rateLimit=60, slot=self.mouse_moved)
        self.proxy2 = pyqtgraph.SignalProxy(self._plot_widget.scene().sigMouseClicked, rateLimit=60, slot=self.on_click)
        return main_window_layout

    def mouse_moved(self, e):
        pos = e[0]
        if self._plot_widget.sceneBoundingRect().contains(pos) and self._is_answer_correct is None:
            mouse_point = self._plot_widget.getPlotItem().vb.mapSceneToView(pos)
            x_position = mouse_point.x()
            y_position = mouse_point.y()

            is_on_function = False
            for function_range in self._function_points_by_expression.values():
                for point_range in function_range:
                    x_range, y_range = point_range
                    is_in_x_range = x_range[0] <= x_position <= x_range[1]
                    is_in_y_range = y_range[0] <= y_position <= y_range[1]
                    is_on_function = is_in_x_range and is_in_y_range

                    if is_on_function:
                        break
                if is_on_function:
                    break

            if is_on_function:
                QApplication.setOverrideCursor(Qt.PointingHandCursor)
            else:
                QApplication.setOverrideCursor(Qt.ArrowCursor)

    def on_click(self, e):
        pos = e[0].pos()
        if self._plot_widget.sceneBoundingRect().contains(pos) and self._is_answer_correct is None:
            mouse_point = self._plot_widget.getPlotItem().vb.mapSceneToView(pos)
            x_position = mouse_point.x() + 0.3
            y_position = mouse_point.y()

            distance_by_expression = {}
            for expression, function_range in self._function_points_by_expression.items():
                for point_range in function_range:
                    x_range, y_range = point_range
                    is_in_x_range = x_range[0] <= x_position <= x_range[1]
                    is_in_y_range = y_range[0] <= y_position <= y_range[1]
                    is_on_function = is_in_x_range and is_in_y_range

                    if is_on_function:
                        x_point = x_range[0] + 0.1
                        y_point = y_range[0] + 0.1
                        distance = math.sqrt(
                            abs((math.pow(x_position - x_point, 2)) - math.pow(y_position - y_point, 2))
                        )
                        distance_by_expression[expression] = abs(distance)
                        break

            if distance_by_expression:
                expression = min(distance_by_expression, key=distance_by_expression.get)
                self._validate_exercise(expression_response=expression)

    def setup_help_data(self):
        self._update_plot_with_help_data()

    def _update_plot_with_help_data(self):
        functions_to_update = self._step.function_help_data.help_expressions
        PlotFactory.update_plot(plot_widget=self._plot_widget, functions_to_update=functions_to_update,
                                is_help_data=True)

    def _validate_exercise(self, expression_response: str):
        self.validate_signal.emit()
        QApplication.setOverrideCursor(Qt.ArrowCursor)
        main_function = self._exercise.get_main_function()
        self._is_answer_correct = main_function.inverse_function.expression == expression_response
        border_color = '#2F8C53' if self._is_answer_correct else 'red'
        if self._is_answer_correct:
            self._help_text.setText('Correcto.')
            self._help_text.setStyleSheet(f'color: {border_color}')
        function = self._exercise.get_function(expression=expression_response) if not self._is_answer_correct \
            else main_function.inverse_function
        color = (0, 128, 0) if self._is_answer_correct else (255, 0, 0)
        PlotFactory.update_plot(plot_widget=self._plot_widget, functions_to_update=[function], rgb_tuple=color)
        if not self._is_answer_correct:
            color = (0, 128, 0)
            PlotFactory.update_plot(plot_widget=self._plot_widget, functions_to_update=[main_function.inverse_function],
                                    rgb_tuple=color)

        self._continue_button.setStyleSheet(f'background: {border_color}')
        self._continue_button.setDisabled(False)
        if not self._is_answer_correct:
            self._update_plot_with_error_data()
        label_functions = [
            (self._exercise.get_main_function(), 'white'),
            (self._exercise.get_main_function().inverse_function, border_color)
        ]
        PlotFactory.add_function_labels(self._plot_widget, label_functions)

    def _update_plot_with_error_data(self):
        self._help_text.setText(f'Incorrecto.')
        self._help_text.setStyleSheet(f'color: red')
        functions_to_update = self._step.function_help_data.help_expressions
        PlotFactory.update_plot(plot_widget=self._plot_widget, functions_to_update=functions_to_update)

    def _send_continue_signal(self):
        self.continue_signal.emit(self._is_answer_correct)

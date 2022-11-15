import math

import pyqtgraph
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QApplication, QSizePolicy

from ..factories import PlotFactory
from ..models.function import Function
from ..models.function_exercise import FunctionExercise
from ..models.function_step import FunctionStep
from ...projectConf.factories import LabelFactory, ButtonFactory
from ...projectConf.factories.icon_factory import IconFactory
from ...projectConf.models.enums.text_type import TextType


class InverseSelectionComponent(QWidget):
    continue_signal = pyqtSignal(bool)
    label = 'Seleccionar la inversa'

    def __init__(self, exercise: FunctionExercise, step: FunctionStep, need_help_data: bool = False):
        super(InverseSelectionComponent, self).__init__()
        self._exercise = exercise
        self._step = step
        self._is_answer_correct = None
        self._function_points_by_expression = {}
        self._need_help_data = need_help_data

        self._plot_widget: pyqtgraph.PlotWidget = None  # noqa
        self._help_subtitle_widget: QLabel = None  # noqa
        self._ok_button: QPushButton = None  # noqa
        self._fail_button: QPushButton = None  # noqa
        self._help_text: QLabel = None  # noqa
        self._help_button: QPushButton = None

        self._layout: QVBoxLayout = None  # noqa
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
        self._layout = QHBoxLayout()
        question_layout = self._get_question_layout()
        self._set_plot_widget(self._exercise)

        self._layout.addLayout(question_layout)
        self._layout.addWidget(self._plot_widget)
        self.setLayout(self._layout)

    def _get_question_layout(self) -> QVBoxLayout:
        question_layout = QVBoxLayout()
        question_layout.setContentsMargins(5, 25, 5, 5)

        question_label = LabelFactory.get_label_component(text=self._step.question, label_type=TextType.BIG_TITLE,
                                                          need_word_wrap=True, align=Qt.AlignHCenter)

        question_layout.addWidget(question_label)
        question_layout.addSpacing(40)

        help_layout = self._get_help_layout()
        question_layout.addLayout(help_layout)

        continue_buttons_layout = self._get_continue_buttons_layout()
        question_layout.addLayout(continue_buttons_layout)
        question_layout.addStretch()

        return question_layout

    def _set_plot_widget(self, exercise: FunctionExercise):
        inverse_function = self._exercise.get_inverse_graph()
        self._plot_widget = PlotFactory.get_plot([*self._exercise.functions, inverse_function], exercise=exercise,
                                                 show_ends=False)

        self.proxy = pyqtgraph.SignalProxy(self._plot_widget.scene().sigMouseMoved, rateLimit=60, slot=self.mouse_moved)
        self.proxy2 = pyqtgraph.SignalProxy(self._plot_widget.scene().sigMouseClicked, rateLimit=60, slot=self.on_click)

    def _get_help_layout(self) -> QVBoxLayout:
        help_layout = QVBoxLayout()

        self._help_text = LabelFactory.get_label_component(text=self._step.function_help_data.help_text,
                                                           label_type=TextType.SUBTITLE,
                                                           align=Qt.AlignHCenter,
                                                           need_word_wrap=True, set_visible=False)

        if self._need_help_data:
            help_button_layout = self._get_help_button_layout()
            help_layout.addLayout(help_button_layout)

        help_layout.addWidget(self._help_text)
        help_layout.addSpacing(35)
        return help_layout

    def _get_help_button_layout(self) -> QVBoxLayout:
        help_button_layout = QVBoxLayout()

        icon = IconFactory.get_icon_widget(image_name='help_button.png')
        self._help_button = ButtonFactory.get_button_component(title='', function_to_connect=self._setup_help_data,
                                                               icon=icon, icon_size=45, tooltip='Ayuda')
        help_button_text = LabelFactory.get_label_component(text='Ayuda', label_type=TextType.NORMAL_TEXT,
                                                            size_policy=(QSizePolicy.Fixed, QSizePolicy.Fixed))

        help_button_layout.addWidget(self._help_button, alignment=Qt.AlignHCenter)
        help_button_layout.addWidget(help_button_text, alignment=Qt.AlignHCenter)
        return help_button_layout

    def _get_continue_buttons_layout(self) -> QHBoxLayout:
        continue_layout = QHBoxLayout()

        icon = IconFactory.get_icon_widget(image_name='continue_button.png')
        self._continue_button = ButtonFactory.get_button_component(
            title='', function_to_connect=lambda: self._send_continue_signal(), icon=icon, icon_size=85,
            tooltip='Continuar', is_disable=True)

        icon = IconFactory.get_icon_widget(image_name='continue_button.png')
        self._back_button = ButtonFactory.get_button_component(
            title='', function_to_connect=lambda: self._send_continue_signal(), icon=icon, icon_size=85,
            tooltip='Ir al ejercicio anterior', is_disable=True)

        continue_layout.addStretch()
        continue_layout.addWidget(self._back_button)
        continue_layout.addStretch()
        continue_layout.addStretch()
        continue_layout.addWidget(self._continue_button)
        continue_layout.addStretch()
        return continue_layout

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

    def _setup_help_data(self):
        self._set_help_text()
        self._update_plot_with_help_data()

    def _set_help_text(self):
        self._help_text.setText(self._step.function_help_data.help_text)
        self._help_text.setStyleSheet(f'color: blue')
        self._help_text.setVisible(True)
        self._help_button.setDisabled(True)

    def _update_plot_with_help_data(self):
        functions_to_update = self._step.function_help_data.help_expressions
        PlotFactory.update_plot(plot_widget=self._plot_widget, functions_to_update=functions_to_update,
                                is_help_data=True, show_ends=False)

    def _validate_exercise(self, expression_response: str):
        QApplication.setOverrideCursor(Qt.ArrowCursor)
        main_function = self._exercise.get_main_function()
        self._is_answer_correct = main_function.inverse_function.expression == expression_response
        border_color = '#2F8C53' if self._is_answer_correct else 'red'
        if self._is_answer_correct:
            self._help_text.setText('Correcto.')
            self._help_text.setStyleSheet(f'color: {border_color}')
        function = self._exercise.get_function_by_expression(expression=expression_response) if not self._is_answer_correct \
            else main_function.inverse_function
        color = (0, 128, 0) if self._is_answer_correct else (255, 0, 0)
        PlotFactory.update_plot(plot_widget=self._plot_widget, functions_to_update=[function], rgb_tuple=color)
        if not self._is_answer_correct:
            color = (0, 128, 0)
            PlotFactory.update_plot(plot_widget=self._plot_widget, functions_to_update=[main_function.inverse_function],
                                    rgb_tuple=color)

        filter_functions = [
            function for function in self._exercise.functions
            if function.expression not in [main_function.expression, expression_response,
                                           main_function.inverse_function.expression]
        ]
        PlotFactory.update_plot(plot_widget=self._plot_widget, functions_to_update=filter_functions,
                                rgb_tuple=(128, 0, 128))

        self._continue_button.setStyleSheet(f'background: {border_color}')
        self._continue_button.setDisabled(False)
        if self._help_button:
            self._help_button.setDisabled(True)
        if not self._is_answer_correct:
            self._update_plot_with_error_data()

        label_functions = [
            (self._exercise.get_main_function(), 'white'),
            (self._exercise.get_main_function().inverse_function, '#2F8C53')
        ]
        PlotFactory.add_function_labels(self._plot_widget, label_functions)

    def _update_plot_with_error_data(self):
        self._help_text.setText(f'Incorrecto. {self._step.function_help_data.help_text}')
        self._help_text.setStyleSheet(f'color: red')
        self._help_text.setVisible(True)
        functions_to_update = self._step.function_help_data.help_expressions
        random_points = self._exercise.get_main_function().get_random_points()
        first_main_point = random_points[len(random_points) // 4]
        first_inverse_point = first_main_point[::-1]

        second_main_point = random_points[len(random_points) // 4 * 3]
        second_inverse_point = second_main_point[::-1]

        PlotFactory.update_plot(plot_widget=self._plot_widget, functions_to_update=functions_to_update)
        PlotFactory.update_plot_with_points(
            plot_widget=self._plot_widget,
            point_function=[[first_main_point, first_inverse_point], [second_main_point, second_inverse_point]],
            rgb_tuple=(47, 140, 83), point_color=(47, 140, 83)
        )

    def _send_continue_signal(self):
        self.continue_signal.emit(self._is_answer_correct)

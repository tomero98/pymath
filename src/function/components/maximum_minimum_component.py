import pyqtgraph
from PyQt5.QtCore import pyqtSignal, Qt, QRegExp
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QLineEdit, QApplication
from pyqt5_plugins.examplebuttonplugin import QtGui

from ..factories import PlotFactory
from ..models.enums.inverse_step_type import InverseStepType
from ..models.function_exercise import FunctionExercise
from ..models.function_step import FunctionStep
from ...projectConf.factories import LabelFactory, ButtonFactory
from ...projectConf.factories.icon_factory import IconFactory
from ...projectConf.factories.line_edit import LineEditFactory
from ...projectConf.models.enums.text_type import TextType


class MaximumMinimumComponent(QWidget):
    continue_signal = pyqtSignal(bool)
    validate_signal = pyqtSignal()

    def __init__(self, exercise: FunctionExercise, step: FunctionStep):
        super(MaximumMinimumComponent, self).__init__()
        self._exercise = exercise
        self._step = step
        self._function_points_by_expression = {}
        self._is_answer_correct = None

        self._plot_widget: pyqtgraph.PlotWidget = None  # noqa
        self._help_subtitle_widget: QLabel = None  # noqa
        self._response_edit: QLineEdit = None  # noqa
        self._help_text: QLabel = None  # noqa
        self._point_label: QLabel = None  # noqa

        self._layout: QVBoxLayout = None  # noqa
        self._main_window_layout: QHBoxLayout = None  # noqa
        self._bottom_buttons_layout: QHBoxLayout = None  # noqa
        self._validate_button: QPushButton = None  # noqa

        self._preload_data()
        self._draw()

    def _preload_data(self):
        for function in self._exercise.functions:
            self._function_points_by_expression[function.expression] = function.get_points_range()

    def _draw(self):
        self._layout = QVBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)

        question_widget = LabelFactory.get_label_component(text=self._step.question, label_type=TextType.SUBTITLE)
        self._point_label = LabelFactory.get_label_component(text='', label_type=TextType.SMALL_TEXT, set_bold=True)
        self._main_window_layout = self._get_main_window_layout(self._exercise)
        self._bottom_buttons_layout = self._get_bottom_buttons_layout()
        self._help_text = LabelFactory.get_label_component(text='', label_type=TextType.NORMAL_TEXT,
                                                           need_word_wrap=True)
        self._validate_button = ButtonFactory.get_button_component(
            title='Comprobar la respuesta', function_to_connect=lambda: self._validate_exercise()
        )

        icon = IconFactory.get_icon_widget(image_name='continue_button.png')
        self._continue_button = ButtonFactory.get_button_component(
            title='', function_to_connect=lambda: self._send_continue_signal(), icon=icon, icon_size=40,
            tooltip='Continuar')

        self._layout.addWidget(question_widget, alignment=Qt.AlignHCenter)
        self._layout.addWidget(self._point_label, alignment=Qt.AlignRight)
        self._layout.addLayout(self._main_window_layout)
        self._layout.addLayout(self._bottom_buttons_layout)
        self._layout.addWidget(self._help_text)
        self._layout.addWidget(self._validate_button, alignment=Qt.AlignHCenter)
        self._layout.addWidget(self._continue_button, alignment=Qt.AlignLeft)
        self.setLayout(self._layout)

    def _get_main_window_layout(self, exercise: FunctionExercise) -> QHBoxLayout:
        main_window_layout = QHBoxLayout()
        self._plot_widget = PlotFactory.get_plot(exercise.functions, show_title=True)
        self.proxy = pyqtgraph.SignalProxy(self._plot_widget.scene().sigMouseMoved, rateLimit=60, slot=self.mouse_moved)
        self.proxy2 = pyqtgraph.SignalProxy(self._plot_widget.scene().sigMouseClicked, rateLimit=60, slot=self.on_click)

        main_window_layout.addStretch()
        main_window_layout.addWidget(self._plot_widget)
        main_window_layout.addStretch()
        return main_window_layout

    def mouse_moved(self, e):
        pos = e[0]
        if self._plot_widget.sceneBoundingRect().contains(pos):
            mouse_point = self._plot_widget.getPlotItem().vb.mapSceneToView(pos)
            x_position = mouse_point.x()
            y_position = mouse_point.y()
            x_position_rounded = round(mouse_point.x(), 1)
            y_position_rounded = round(mouse_point.y(), 1)
            self._point_label.setText(f'Punto ({x_position_rounded}, {y_position_rounded})')

            is_on_function = False
            for function_range in self._function_points_by_expression.values():
                for point_range in function_range:
                    x_range, y_range = point_range
                    is_in_x_range = round(x_range[0], 1) <= x_position <= round(x_range[1], 1)
                    is_in_y_range = round(y_range[0], 1) <= y_position <= round(y_range[1], 1)

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
        if self._plot_widget.sceneBoundingRect().contains(pos):
            mouse_point = self._plot_widget.getPlotItem().vb.mapSceneToView(pos)
            x_position = mouse_point.x() + 0.3
            y_position = mouse_point.y()

            for expression, function_range in self._function_points_by_expression.items():
                for point_range in function_range:
                    x_range, y_range = point_range
                    is_in_x_range = round(x_range[0], 1) <= x_position <= round(x_range[1], 1)
                    is_in_y_range = round(y_range[0], 1) <= y_position <= round(y_range[1], 1)
                    is_on_function = is_in_x_range and is_in_y_range

                    if is_on_function:
                        self._on_click_point()
                        break

    def _on_click_point(self):
        point = self._point_label.text()[5:]
        if self._step.type in [InverseStepType.maximum_relative_exercise, InverseStepType.minimum_relative_exercise]:
            self._response_edit.setText(f'{self._response_edit.text()}{point}; ')
        else:
            self._response_edit.setText(f'{point}')

    def _get_bottom_buttons_layout(self) -> QHBoxLayout:
        layout = QVBoxLayout()
        response_layout = self._get_response_layout()
        layout.addLayout(response_layout)
        return layout

    def _get_response_layout(self) -> QHBoxLayout:
        response_layout = QHBoxLayout()
        is_absolute = self._step.type in [InverseStepType.minimum_absolute_exercise,
                                          InverseStepType.maximum_absolute_exercise]
        input_placeholder = '(5, 4)' if is_absolute else '(5, 4); (5, 1)'
        self._response_edit = LineEditFactory.get_line_edit_component(placeholder_text=input_placeholder)
        regex_absolute = QRegExp('([0-9,]*[\ ]*,[\ ]*[0-9,]*)')
        regex_relative = QRegExp('([0-9,]*[\ ]*,[\ ]*[0-9,]*);' * 4)
        regex = regex_absolute if is_absolute else regex_relative
        validator = QtGui.QRegExpValidator(regex)
        self._response_edit.setValidator(validator)
        response_text = 'Introduzca el punto asociado: ' if is_absolute else 'Introduzca los puntos asociados: '
        response_label = LabelFactory.get_label_component(text=response_text, label_type=TextType.NORMAL_TEXT)
        response_layout.addWidget(response_label)
        response_layout.addWidget(self._response_edit)
        return response_layout

    def setup_help_data(self):
        self._set_help_text()

    def _set_help_text(self):
        self._help_text.setText(self._step.function_help_data.help_text)
        self._help_text.setStyleSheet(f'color: blue')

    def _validate_exercise(self):
        self._is_answer_correct = True
        border_color = '#2F8C53' if self._is_answer_correct else 'red'
        self._validate_button.setStyleSheet(f'background: {border_color}')
        self._response_edit.setStyleSheet(f'background: {border_color}')
        self._continue_button.setStyleSheet(f'background: {border_color}')
        if not self._is_answer_correct:
            self._update_plot_with_error_data()

    def _update_plot_with_error_data(self):
        self._help_text.setText(f'Recuerda que: "{self._step.function_help_data.help_text}". Por lo que en este caso '
                                f'habría que delimitar el dominio de la función.')
        self._help_text.setStyleSheet(f'color: red')

    def _send_continue_signal(self):
        if self._is_answer_correct is not None:
            self.continue_signal.emit(True)
        else:
            self._validate_exercise()

import pyqtgraph
from PyQt5.QtCore import pyqtSignal, Qt, QRegExp
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QLineEdit, QApplication, QSizePolicy
from pyqt5_plugins.examplebuttonplugin import QtGui

from ..factories import PlotFactory
from ..models.function_exercise import FunctionExercise
from ..models.function_step import FunctionStep
from ...projectConf.factories import LabelFactory, ButtonFactory
from ...projectConf.factories.icon_factory import IconFactory
from ...projectConf.factories.line_edit import LineEditFactory
from ...projectConf.models.enums.text_type import TextType


class MaximumMinimumComponent(QWidget):
    continue_signal = pyqtSignal()

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
        self._point_label = LabelFactory.get_label_component(text='Coordenada x: ', label_type=TextType.SUBTITLE,
                                                             set_bold=True, set_visible=False)
        self._validate_button_layout = self._get_validate_button_layout()
        self._validate_button = ButtonFactory.get_button_component(
            title='Comprobar la respuesta', function_to_connect=lambda: self._validate_exercise()
        )
        self._bottom_buttons_layout = self._get_bottom_buttons_layout()

        question_layout.addWidget(question_label)
        question_layout.addSpacing(40)
        question_layout.addLayout(self._bottom_buttons_layout)
        question_layout.addWidget(self._point_label, alignment=Qt.AlignHCenter)
        question_layout.addSpacing(40)
        question_layout.addLayout(self._validate_button_layout)

        continue_buttons_layout = self._get_continue_buttons_layout()
        question_layout.addLayout(continue_buttons_layout)
        question_layout.addStretch()

        return question_layout

    def _set_plot_widget(self, exercise: FunctionExercise):
        self._plot_widget = PlotFactory.get_plot(exercise.functions, exercise=exercise, show_ends=False)
        self.proxy = pyqtgraph.SignalProxy(self._plot_widget.scene().sigMouseMoved, rateLimit=60, slot=self.mouse_moved)
        self.proxy2 = pyqtgraph.SignalProxy(self._plot_widget.scene().sigMouseClicked, rateLimit=60, slot=self.on_click)

    def _get_validate_button_layout(self) -> QVBoxLayout:
        validate_button_layout = QVBoxLayout()

        icon = IconFactory.get_icon_widget(image_name='comprobar_respuesta.png')
        self._validate_button = ButtonFactory.get_button_component(
            title='', function_to_connect=lambda: self._validate_exercise(), icon=icon, icon_size=50,
            tooltip='Validar respuesta',
        )
        validate_button_text = LabelFactory.get_label_component(text='Comprobar respuesta',
                                                                label_type=TextType.NORMAL_TEXT,
                                                                size_policy=(QSizePolicy.Fixed, QSizePolicy.Fixed))

        validate_button_layout.addWidget(self._validate_button, alignment=Qt.AlignHCenter)
        validate_button_layout.addWidget(validate_button_text, alignment=Qt.AlignHCenter)
        return validate_button_layout

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
        point = self._point_label.text()[6:]
        x_value = point[1:-1].split(',')[0]
        self._response_edit.setText(f'{self._response_edit.text()}{x_value}; ')

    def _get_bottom_buttons_layout(self) -> QVBoxLayout:
        layout = QVBoxLayout()
        response_layout = self._get_response_layout()
        text = 'El formato esperado para introducir las abscisas es el siguiente: "-1; 5;".'
        placeholder = LabelFactory.get_label_component(text=text, label_type=TextType.NORMAL_TEXT, set_cursive=True)
        layout.addWidget(placeholder, alignment=Qt.AlignHCenter)
        layout.addLayout(response_layout)
        return layout

    def _get_response_layout(self) -> QHBoxLayout:
        response_layout = QVBoxLayout()
        input_placeholder = '-1; 5;'
        self._response_edit = LineEditFactory.get_line_edit_component(placeholder_text=input_placeholder, font_size=22,
                                                                      fixed_height=60)
        regex = QRegExp('[\-]?[0-9]*[\ ]*;[\ ]*[\-]?[0-9]*;[\ ]*' * 4)
        validator = QtGui.QRegExpValidator(regex)
        self._response_edit.setValidator(validator)
        response_layout.addWidget(self._response_edit)
        return response_layout

    def _validate_exercise(self):
        self._is_answer_correct = True
        border_color = '#2F8C53' if self._is_answer_correct else 'red'
        self._validate_button.setStyleSheet(f'background: {border_color}')
        self._response_edit.setStyleSheet(f'background: {border_color}')
        self._continue_button.setStyleSheet(f'background: {border_color}')
        if not self._is_answer_correct:
            self._update_plot_with_error_data()

    def _update_plot_with_error_data(self):
        print(5)

    def _send_continue_signal(self):
        if self._is_answer_correct is not None:
            self.continue_signal.emit()
        else:
            self._validate_exercise()

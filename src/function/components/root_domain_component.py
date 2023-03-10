import pyqtgraph
from PyQt5.QtCore import pyqtSignal, Qt, QRegExp
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QSizePolicy
from pyqt5_plugins.examplebuttonplugin import QtGui

from ..factories import PlotFactory
from ..models.function_exercise import FunctionExercise
from ..models.function_step import FunctionStep
from ...projectConf.factories import LabelFactory, ButtonFactory
from ...projectConf.factories.icon_factory import IconFactory
from ...projectConf.factories.line_edit_factory import LineEditFactory
from ...projectConf.models.enums.text_type import TextType


class RootDomainComponent(QWidget):
    continue_signal = pyqtSignal()

    def __init__(self, exercise: FunctionExercise, step: FunctionStep, need_help_data: bool = True):
        super(RootDomainComponent, self).__init__()
        self._exercise = exercise
        self._step = step
        self._is_answer_correct = True
        self._need_help_data = need_help_data
        self._function_points_by_expression = {}

        self._plot_widget: pyqtgraph.PlotWidget = None
        self._help_subtitle_widget: QLabel = None
        self._ok_button: QPushButton = None
        self._fail_button: QPushButton = None
        self._help_text: QLabel = None

        self._layout: QVBoxLayout = None
        self._main_window_layout: QHBoxLayout = None
        self._bottom_buttons_layout: QHBoxLayout = None

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

        question_label = LabelFactory.get_label_component(text=self._step.question, label_type=TextType.TITLE,
                                                          need_word_wrap=True, align=Qt.AlignHCenter)
        self._point_label = LabelFactory.get_label_component(
            text=f'Punto (0, 0)', label_type=TextType.SUBTITLE, set_bold=True, set_visible=False
        )
        buttons_layout = self._get_bottom_buttons_layout()

        question_layout.addWidget(question_label, alignment=Qt.AlignHCenter)
        question_layout.addSpacing(40)
        question_layout.addLayout(buttons_layout)
        question_layout.addWidget(self._point_label, alignment=Qt.AlignHCenter)
        question_layout.addSpacing(40)

        help_text_layout = QVBoxLayout()

        validate_layout = self._get_validate_button_layout()

        middle_buttons_layout = QHBoxLayout()
        middle_buttons_layout.addStretch()
        if self._need_help_data:
            help_layout = self._get_help_layout()
            middle_buttons_layout.addLayout(help_layout)
            middle_buttons_layout.addStretch()
        middle_buttons_layout.addLayout(validate_layout)
        middle_buttons_layout.addStretch()

        self._help_text = LabelFactory.get_label_component(text=self._step.function_help_data.help_text,
                                                           label_type=TextType.SUBTITLE,
                                                           align=Qt.AlignHCenter,
                                                           need_word_wrap=True, set_visible=False)
        help_text_layout.addLayout(middle_buttons_layout)
        help_text_layout.addWidget(self._help_text)

        question_layout.addLayout(help_text_layout)

        continue_buttons_layout = self._get_continue_buttons_layout()
        question_layout.addLayout(continue_buttons_layout)
        question_layout.addStretch()

        return question_layout

    def _set_plot_widget(self, exercise: FunctionExercise):
        self._plot_widget = PlotFactory.get_plot(exercise.functions, exercise=exercise, show_title=True)
        self.proxy = pyqtgraph.SignalProxy(self._plot_widget.scene().sigMouseMoved, rateLimit=60, slot=self.mouse_moved)
        self.proxy2 = pyqtgraph.SignalProxy(self._plot_widget.scene().sigMouseClicked, rateLimit=60, slot=self.on_click)

    def _get_help_layout(self) -> QVBoxLayout:
        help_layout = QVBoxLayout()
        help_button_layout = self._get_help_button_layout()
        help_layout.addLayout(help_button_layout)
        help_layout.addSpacing(35)
        return help_layout

    def _get_help_button_layout(self) -> QVBoxLayout:
        help_button_layout = QVBoxLayout()

        icon = IconFactory.get_icon_widget(image_name='help_button.png')
        self._help_button = ButtonFactory.get_button_component(title='', function_to_connect=self._setup_help_data,
                                                               icon=icon, icon_size=50, tooltip='Ayuda')
        help_button_text = LabelFactory.get_label_component(text='Ayuda', label_type=TextType.NORMAL_TEXT,
                                                            size_policy=(QSizePolicy.Fixed, QSizePolicy.Fixed))

        help_button_layout.addWidget(self._help_button, alignment=Qt.AlignHCenter)
        help_button_layout.addWidget(help_button_text, alignment=Qt.AlignHCenter)
        return help_button_layout

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

    def _get_main_window_layout(self, exercise: FunctionExercise) -> QHBoxLayout:
        main_window_layout = QHBoxLayout()
        self._plot_widget = PlotFactory.get_plot(exercise.functions, exercise=exercise, show_title=True)
        self.proxy = pyqtgraph.SignalProxy(self._plot_widget.scene().sigMouseMoved, rateLimit=60, slot=self.mouse_moved)

        main_window_layout.addStretch()
        main_window_layout.addWidget(self._plot_widget)
        main_window_layout.addStretch()
        return main_window_layout

    def mouse_moved(self, e):
        pos = e[0]
        if self._plot_widget.sceneBoundingRect().contains(pos):
            mouse_point = self._plot_widget.getPlotItem().vb.mapSceneToView(pos)
            x_position = round(mouse_point.x(), 2)
            y_position = round(mouse_point.y(), 2)
            self._point_label.setText(f'Punto ({x_position}, {y_position})')
            self._point_label.setVisible(True)

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

    def _get_bottom_buttons_layout(self) -> QHBoxLayout:
        layout = QVBoxLayout()
        domain_layout = self._get_response_layout()
        text = 'El formato esperado es el siguiente: "0; 9;".'
        placeholder = LabelFactory.get_label_component(text=text, label_type=TextType.NORMAL_TEXT, set_cursive=True)
        layout.addLayout(domain_layout)
        layout.addWidget(placeholder, alignment=Qt.AlignHCenter)
        return layout

    def _get_response_layout(self) -> QHBoxLayout:
        response_layout = QVBoxLayout()
        input_placeholder = '0; 9;'
        self._response_edit = LineEditFactory.get_line_edit_component(placeholder_text=input_placeholder)
        regex = QRegExp('[\-]?[0-9]*[\ ]*;[\ ]*[\-]?[0-9]*;[\ ]*' * 4)
        validator = QtGui.QRegExpValidator(regex)
        self._response_edit.setValidator(validator)
        response_text = 'Introduzca las abscisas asociadas: '
        response_label = LabelFactory.get_label_component(text=response_text, label_type=TextType.SUBTITLE)
        response_layout.addWidget(response_label, alignment=Qt.AlignHCenter)
        response_layout.addWidget(self._response_edit)
        return response_layout

    def _setup_help_data(self):
        self._set_help_text()

    def _set_help_text(self):
        self._help_text.setText(self._step.function_help_data.help_text)
        self._help_text.setStyleSheet(f'color: blue')
        self._help_text.setVisible(True)
        self._help_button.setDisabled(True)

    def _validate_exercise(self):
        bounded_range = self._exercise.has_bounded_range()
        self._is_answer_correct = bounded_range
        border_color = '#2F8C53' if self._is_answer_correct else 'red'
        if self._is_answer_correct:
            self._help_text.setText('Correcto.')
            self._help_text.setStyleSheet(f'color: {border_color}')
            self._help_text.setVisible(True)
        self._continue_button.setStyleSheet(f'background: {border_color}')
        self._continue_button.setDisabled(False)
        self._ok_button.setDisabled(True)
        self._fail_button.setDisabled(True)
        if not self._is_answer_correct:
            self._update_plot_with_error_data()
        if self._help_button:
            self._help_button.setDisabled(True)

    def _update_plot_with_error_data(self):
        self._help_text.setText(f'Incorrecto. {self._step.function_help_data.help_text}')
        self._help_text.setStyleSheet(f'color: red')
        self._help_text.setVisible(True)

    def _send_continue_signal(self):
        self.continue_signal.emit()

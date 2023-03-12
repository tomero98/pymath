import pyqtgraph
from PyQt5.QtCore import pyqtSignal, Qt, QRegExp
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QLineEdit, QSizePolicy
from pyqt5_plugins.examplebuttonplugin import QtGui

from src.function.factories import PlotFactory
from src.function.models.enums.step_type import StepType
from src.function.models.function_exercise import FunctionExercise
from src.function.models.function_step import FunctionStep
from src.projectConf.factories import LabelFactory, ButtonFactory
from src.projectConf.factories.icon_factory import IconFactory
from src.projectConf.factories.line_edit_factory import LineEditFactory
from src.projectConf.models.enums.text_type import TextType


class DomainIndicateComponent(QWidget):
    continue_signal = pyqtSignal()
    validate_signal = pyqtSignal()

    def __init__(self, exercise: FunctionExercise, step: FunctionStep, need_help_data: bool = True):
        super(DomainIndicateComponent, self).__init__()
        self._exercise = exercise
        self._step = step
        self._is_answer_correct = True
        self._need_help_data = need_help_data
        self._is_domain_exercise = step.type == StepType.indicate_domain_exercise
        self._is_range_exercise = step.type == StepType.indicate_range_exercise

        self._plot_widget: pyqtgraph.PlotWidget = None  # noqa
        self._help_subtitle_widget: QLabel = None  # noqa
        self._domain_edit: QLineEdit = None  # noqa
        self._range_edit: QLineEdit = None  # noqa
        self._help_text: QLabel = None  # noqa
        self._point_label: QLabel = None  # noqa

        self._layout: QVBoxLayout = None  # noqa
        self._main_window_layout: QHBoxLayout = None  # noqa
        self._bottom_buttons_layout: QHBoxLayout = None  # noqa
        self._validate_button: QPushButton = None  # noqa

        self._draw()

    @property
    def label(self):
        if self._step.type == StepType.indicate_domain_exercise:
            label = 'Indicar el dominio.'
        elif self._step.type == StepType.indicate_range_exercise:
            label = 'Indicar el rango.'
        # elif self._step.type == StepType.indicate_bounded_range_exercise:
        #     label = 'Indicar si la función está acotada.'
        # elif self._step.type == StepType.indicate_roots_exercise:
        #     label = 'Indicar si las raíces de la función.'
        return label

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
        self._point_label = LabelFactory.get_label_component(
            text=f'Punto (0, 0)', label_type=TextType.SUBTITLE, set_bold=True, set_visible=False
        )
        buttons_layout = self._get_bottom_buttons_layout()

        question_layout.addWidget(question_label, alignment=Qt.AlignHCenter)
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
        self._plot_widget = PlotFactory.get_plot(exercise.functions, exercise=exercise, show_title=True,
                                                 rgb_tuple=(255, 255, 255))
        self.proxy = pyqtgraph.SignalProxy(self._plot_widget.scene().sigMouseMoved, rateLimit=60, slot=self.mouse_moved)

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

    def _get_bottom_buttons_layout(self) -> QHBoxLayout:
        layout = QVBoxLayout()
        domain_layout = self._get_domain_layout()
        text = 'El formato esperado es similar al siguiente siguiente: "(-inf, 8] U (1, +inf) U {5}".'
        placeholder = LabelFactory.get_label_component(text=text, label_type=TextType.SUBTITLE, set_cursive=True,
                                                       need_word_wrap=True)
        layout.addWidget(placeholder, alignment=Qt.AlignHCenter)
        layout.addLayout(domain_layout)
        return layout

    def _get_domain_layout(self) -> QVBoxLayout:
        domain_layout = QVBoxLayout()
        input_placeholder = '(-inf, 8] U (1, +inf)'
        self._domain_edit = LineEditFactory.get_line_edit_component(placeholder_text=input_placeholder, fixed_height=60,
                                                                    font_size=28)
        regex = QRegExp('[\(\[0-9\-][\ ]*[\-+inf0-9]+[\ ]*,[\ ]*[\-+inf0-9]+[\ ]*[\)\]][\ ]*U[\ ]*' * 5)
        validator = QtGui.QRegExpValidator(regex)
        self._domain_edit.setValidator(validator)
        domain_layout.addWidget(self._domain_edit)
        return domain_layout

    def _setup_help_data(self):
        self._set_help_text()
        self._update_plot_with_help_data()

    def _set_help_text(self):
        self._help_text.setText(self._step.function_help_data.help_text)
        self._help_text.setStyleSheet(f'color: blue')
        self._help_text.setVisible(True)
        self._help_button.setDisabled(True)

    def _update_plot_with_help_data(self):
        x_values, y_values = self._exercise.get_domain_range_values(small_sample=True)
        points = []
        if self._is_domain_exercise:
            values = [(x, y) for x, y in zip(x_values, y_values) if -5 < x < 5 and -5 < y < 5]
            for x_value, y_value in values:
                points.append([(x_value, y_value), (0, y_value)])
        else:
            pass
        PlotFactory.update_plot_with_points(plot_widget=self._plot_widget, point_function=points, no_points=True,
                                            rgb_tuple=(0, 0, 255), pen_width=2)

    def _validate_exercise(self):
        self._validate_button.setDisabled(True)
        expression = self._domain_edit.text()
        domain_is_correct = self._exercise.validate_domain_expression(domain_expression=expression) \
            if self._is_domain_exercise \
            else self._exercise.validate_range_expression(range_expression=expression)
        self._is_answer_correct = domain_is_correct
        border_color = '#2F8C53' if self._is_answer_correct else 'red'
        if not domain_is_correct:
            self._domain_edit.setText(f'{self._domain_edit.text()} != {self._exercise.get_domain_expression()}')
        domain_color = '#2F8C53' if domain_is_correct else 'red'
        self._validate_button.setStyleSheet(f'background: {border_color}')
        self._domain_edit.setStyleSheet(f'background: {domain_color}; font-size: 28px')
        self._continue_button.setDisabled(False)
        if not self._is_answer_correct:
            self._update_plot_with_error_data()
        if self._help_button:
            self._help_button.setDisabled(True)

        help_text = 'Correcto.' if domain_is_correct else f'Incorrecto. {self._step.function_help_data.help_text}'
        self._help_text.setText(help_text)
        self._help_text.setStyleSheet(f'color: {border_color}')
        self._help_text.setVisible(True)

    def _update_plot_with_error_data(self):
        functions_to_update = self._step.function_help_data.help_expressions
        PlotFactory.update_plot(plot_widget=self._plot_widget, functions_to_update=functions_to_update, no_points=True,
                                constants=True)

    def _send_continue_signal(self):
        self.continue_signal.emit()

import pyqtgraph
from PyQt5.QtCore import pyqtSignal, Qt, QRegExp
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QLineEdit
from pyqt5_plugins.examplebuttonplugin import QtGui

from ..factories import PlotFactory
from ..models.function_exercise import FunctionExercise
from ..models.function_step import FunctionStep
from ...projectConf.factories import LabelFactory, ButtonFactory
from ...projectConf.factories.icon_factory import IconFactory
from ...projectConf.factories.line_edit import LineEditFactory
from ...projectConf.models.enums.text_type import TextType


class DomainIndicateComponent(QWidget):
    continue_signal = pyqtSignal(bool)
    validate_signal = pyqtSignal()

    def __init__(self, exercise: FunctionExercise, step: FunctionStep):
        super(DomainIndicateComponent, self).__init__()
        self._exercise = exercise
        self._step = step
        self._is_answer_correct = True

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
            tooltip='Continuar', is_disable=True)


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

    def _get_bottom_buttons_layout(self) -> QHBoxLayout:
        layout = QVBoxLayout()

        domain_layout = self._get_domain_layout()
        range_layout = self._get_range_layout()

        layout.addLayout(domain_layout)
        layout.addLayout(range_layout)
        return layout

    def _get_domain_layout(self) -> QHBoxLayout:
        domain_layout = QHBoxLayout()
        input_placeholder = '(-inf, 8] U (1, +inf)'
        self._domain_edit = LineEditFactory.get_line_edit_component(placeholder_text=input_placeholder)
        regex = QRegExp('[\(\[0-9\-][\ ]*[\-+inf0-9]+[\ ]*,[\ ]*[\-+inf0-9]+[\ ]*[\)\]][\ ]*U[\ ]*' * 5)
        validator = QtGui.QRegExpValidator(regex)
        self._domain_edit.setValidator(validator)
        domain_text = 'Introduzca el dominio de la función: '
        domain_label = LabelFactory.get_label_component(text=domain_text, label_type=TextType.NORMAL_TEXT)
        domain_layout.addWidget(domain_label)
        domain_layout.addWidget(self._domain_edit)
        return domain_layout

    def _get_range_layout(self) -> QHBoxLayout:
        range_layout = QHBoxLayout()
        input_placeholder = '5 U (3, -2]'
        self._range_edit = LineEditFactory.get_line_edit_component(placeholder_text=input_placeholder)
        regex = QRegExp('[\(\[0-9\-][\ ]*[\-+inf0-9]+[\ ]*,[\ ]*[\-+inf0-9]+[\ ]*[\)\]][\ ]*U[\ ]*' * 5)
        validator = QtGui.QRegExpValidator(regex)
        self._range_edit.setValidator(validator)
        range_text = 'Introduzca el rango de la función: '
        range_label = LabelFactory.get_label_component(text=range_text, label_type=TextType.NORMAL_TEXT)
        range_layout.addWidget(range_label)
        range_layout.addWidget(self._range_edit)
        return range_layout

    def setup_help_data(self):
        self._set_help_text()
        self._update_plot_with_help_data()

    def _set_help_text(self):
        self._help_text.setText(self._step.function_help_data.help_text)
        self._help_text.setStyleSheet(f'color: blue')

    def _update_plot_with_help_data(self):
        functions_to_update = self._step.function_help_data.help_expressions
        PlotFactory.update_plot(plot_widget=self._plot_widget, functions_to_update=functions_to_update,
                                is_help_data=True, no_points=True, constants=True)

    def _validate_exercise(self):
        domain_expression = self._domain_edit.text()
        domain_is_correct = self._exercise.validate_domain_expression(domain_expression=domain_expression)
        range_expression = self._range_edit.text()
        range_is_correct = self._exercise.validate_range_expression(range_expression=range_expression)
        self._is_answer_correct = domain_is_correct and range_is_correct
        border_color = '#2F8C53' if self._is_answer_correct else 'red'
        if not domain_is_correct:
            self._domain_edit.setText(f'{self._domain_edit.text()} != {self._exercise.get_domain_expression()}')
        domain_color = '#2F8C53' if domain_is_correct else 'red'
        if not range_is_correct:
            self._range_edit.setText(f'{self._range_edit.text()} != {self._exercise.get_range_expression()}')
        range_color = '#2F8C53' if range_is_correct else 'red'
        self._validate_button.setStyleSheet(f'background: {border_color}')
        self._domain_edit.setStyleSheet(f'background: {domain_color}')
        self._range_edit.setStyleSheet(f'background: {range_color}')
        self._continue_button.setDisabled(False)
        if not self._is_answer_correct:
            self._update_plot_with_error_data()

    def _update_plot_with_error_data(self):
        self._help_text.setText(f'Recuerda que: "{self._step.function_help_data.help_text}". Por lo que en este caso '
                                f'habría que delimitar el dominio de la función.')
        self._help_text.setStyleSheet(f'color: red')
        functions_to_update = self._step.function_help_data.help_expressions
        PlotFactory.update_plot(plot_widget=self._plot_widget, functions_to_update=functions_to_update, no_points=True,
                                constants=True)

    def _send_continue_signal(self):
        self.continue_signal.emit(self._is_answer_correct)

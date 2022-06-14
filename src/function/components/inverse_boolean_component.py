import pyqtgraph
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout

from ..factories import PlotFactory
from ..models.function_exercise import FunctionExercise
from ..models.function_step import FunctionStep
from ...projectConf.factories import LabelFactory, ButtonFactory
from ...projectConf.models.enums.text_type import TextType


class InverseBooleanComponent(QWidget):
    continue_signal = pyqtSignal(bool)

    def __init__(self, exercise: FunctionExercise, step: FunctionStep):
        super(InverseBooleanComponent, self).__init__()
        self._exercise = exercise
        self._step = step
        self._is_answer_correct = True

        self._plot_widget: pyqtgraph.PlotWidget = None
        self._help_subtitle_widget: QLabel = None
        self._ok_button: QPushButton = None
        self._fail_button: QPushButton = None
        self._help_text: QLabel = None

        self._layout: QVBoxLayout = None
        self._main_window_layout: QHBoxLayout = None
        self._bottom_buttons_layout: QHBoxLayout = None

        self._draw()

    def _draw(self):
        self._layout = QVBoxLayout()
        question_widget = LabelFactory.get_label_component(text=self._step.question, label_type=TextType.SUBTITLE)
        self._main_window_layout = self._get_main_window_layout(self._exercise)
        self._bottom_buttons_layout = self._get_bottom_buttons_layout()
        self._help_text = LabelFactory.get_label_component(text='', label_type=TextType.NORMAL_TEXT)
        self._continue_button = ButtonFactory.get_button_component(
            title='Continuar', function_to_connect=lambda: self._send_continue_signal(), is_disable=True
        )
        self._layout.addWidget(question_widget)
        self._layout.addLayout(self._main_window_layout)
        self._layout.addLayout(self._bottom_buttons_layout)
        self._layout.addWidget(self._help_text)
        self._layout.addWidget(self._continue_button, alignment=Qt.AlignRight)
        self.setLayout(self._layout)

    def _get_main_window_layout(self, exercise: FunctionExercise) -> QHBoxLayout:
        main_window_layout = QHBoxLayout()
        self._plot_widget = PlotFactory.get_plot([exercise.get_main_function()])

        main_window_layout.addStretch()
        main_window_layout.addWidget(self._plot_widget)
        main_window_layout.addStretch()
        return main_window_layout

    def _get_bottom_buttons_layout(self) -> QHBoxLayout:
        layout = QHBoxLayout()

        self._ok_button = ButtonFactory.get_button_component(
            title='Sí',
            function_to_connect=lambda: self._validate_exercise(response=True, pressed_button=self._ok_button)
        )
        self._fail_button = ButtonFactory.get_button_component(
            title='No',
            function_to_connect=lambda: self._validate_exercise(response=False, pressed_button=self._fail_button)
        )

        layout.addStretch()
        layout.addWidget(self._ok_button)
        layout.addStretch()
        layout.addWidget(self._fail_button)
        layout.addStretch()
        return layout

    def setup_help_data(self):
        self._set_help_text()
        self._update_plot_with_help_data()

    def _set_help_text(self):
        self._help_text.setText(self._step.function_help_data.help_text)
        self._help_text.setStyleSheet(f'color: blue')

    def _update_plot_with_help_data(self):
        current_functions = self._exercise.get_main_function()
        functions_to_update = self._step.function_help_data.help_expressions
        PlotFactory.update_plot(plot_widget=self._plot_widget, current_functions=[current_functions],
                                functions_to_update=functions_to_update, is_help_data=True)

    def _validate_exercise(self, response: bool, pressed_button: QPushButton):
        has_function_inverse = self._exercise.has_main_function_inverse()
        self._is_answer_correct = has_function_inverse == response
        border_color = 'green' if self._is_answer_correct else 'red'
        pressed_button.setStyleSheet(f'border: 3px solid {border_color}')
        self._plot_widget.setStyleSheet(f'border: 3px solid {border_color}')
        self._continue_button.setDisabled(False)
        if not self._is_answer_correct:
            self._update_plot_with_error_data()

    def _update_plot_with_error_data(self):
        self._help_text.setText(f'Recuerda que: "{self._step.function_help_data.help_text}". Por lo que en este caso '
                                f'habría que delimitar el dominio de la función.')
        self._help_text.setStyleSheet(f'color: red')
        current_functions = self._exercise.get_main_function()
        functions_to_update = self._step.function_help_data.help_expressions
        PlotFactory.update_plot(plot_widget=self._plot_widget, current_functions=[current_functions],
                                functions_to_update=functions_to_update)

    def _send_continue_signal(self):
        self.continue_signal.emit(self._is_answer_correct)

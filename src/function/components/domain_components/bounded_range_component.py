import pyqtgraph
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QSizePolicy

from src.function.factories import PlotFactory
from src.function.models.function_exercise import FunctionExercise
from src.function.models.function_step import FunctionStep
from src.projectConf.factories import LabelFactory, ButtonFactory
from src.projectConf.factories.icon_factory import IconFactory
from src.projectConf.models.enums.text_type import TextType


class BoundedRangeComponent(QWidget):
    continue_signal = pyqtSignal()

    def __init__(self, exercise: FunctionExercise, step: FunctionStep, need_help_data: bool = True):
        super(BoundedRangeComponent, self).__init__()
        self._exercise = exercise
        self._step = step
        self._is_answer_correct = True
        self._need_help_data = need_help_data

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

        self._bottom_buttons_layout = self._get_bottom_buttons_layout()

        question_layout.addWidget(question_label)
        question_layout.addSpacing(40)
        question_layout.addLayout(self._bottom_buttons_layout)
        question_layout.addSpacing(40)

        help_layout = self._get_help_layout()
        question_layout.addLayout(help_layout)

        continue_buttons_layout = self._get_continue_buttons_layout()
        question_layout.addLayout(continue_buttons_layout)
        question_layout.addStretch()

        return question_layout

    def _set_plot_widget(self, exercise: FunctionExercise):
        self._plot_widget = PlotFactory.get_plot(exercise.functions, exercise=exercise, rgb_tuple=(255, 255, 255))

    def _get_bottom_buttons_layout(self) -> QHBoxLayout:
        layout = QHBoxLayout()

        self._ok_button = ButtonFactory.get_button_component(
            title='Sí', minimum_width=90, minimum_height=90, text_size=22, tooltip='Sí',
            function_to_connect=lambda: self._validate_exercise(response=True, pressed_button=self._ok_button)
        )

        self._fail_button = ButtonFactory.get_button_component(
            title='No', minimum_width=90, minimum_height=90, text_size=22, tooltip='No',
            function_to_connect=lambda: self._validate_exercise(response=False, pressed_button=self._fail_button)
        )

        layout.addStretch()
        layout.addWidget(self._ok_button)
        layout.addStretch()
        layout.addWidget(self._fail_button)
        layout.addStretch()
        return layout

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

    def _setup_help_data(self):
        self._set_help_text()
        self._help_button.setDisabled(True)

    def _set_help_text(self):
        self._help_text.setText(self._step.function_help_data.help_text)
        self._help_text.setStyleSheet(f'color: blue')
        self._help_text.setVisible(True)

    def _validate_exercise(self, response: bool, pressed_button: QPushButton):
        bounded_range = self._exercise.has_bounded_range()
        self._is_answer_correct = bounded_range == response
        border_color = '#2F8C53' if self._is_answer_correct else 'red'
        if self._is_answer_correct:
            self._help_text.setText('Correcto.')
            self._help_text.setStyleSheet(f'color: {border_color}')
            self._help_text.setVisible(True)
        pressed_button.setStyleSheet(f'background: {border_color}')
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

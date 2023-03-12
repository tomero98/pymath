from typing import List

import pyqtgraph
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QPushButton, QHBoxLayout

from .component import Component
from ..factories import PlotFactory
from ..models.enums.resume_state import ResumeState
from ..models.exercise_resume import ExerciseResume
from ..models.function_exercise import FunctionExercise
from ..models.function_step import FunctionStep
from ...projectConf.factories import LabelFactory, ButtonFactory
from ...projectConf.factories.icon_factory import IconFactory
from ...projectConf.models.enums.text_type import TextType


class SelectionComponent(Component):
    resume_signal = pyqtSignal(ExerciseResume)

    def __init__(self, exercise: FunctionExercise, step: FunctionStep, resume: ExerciseResume,
                 need_help_data: bool = False, show_main_function_limits: bool = False,
                 show_function_labels: bool = False):
        super(SelectionComponent, self).__init__(
            exercise=exercise, step=step, resume=resume, need_help_data=need_help_data,
            show_main_function_limits=show_main_function_limits, show_function_labels=show_function_labels
        )

        self._plot_widget: pyqtgraph.PlotWidget = None  # noqa
        self._help_subtitle_widget: QLabel = None  # noqa
        self._graph_buttons: List[QPushButton] = []  # noqa
        self._help_text: QLabel = None  # noqa
        self._layout: QVBoxLayout = None  # noqa
        self._main_window_layout: QHBoxLayout = None  # noqa
        self._bottom_buttons_layout: QHBoxLayout = None  # noqa

    def _setup_data(self):
        pass

    def _draw(self):
        self._layout = QHBoxLayout()
        question_layout = self._get_question_layout()
        self._set_plot_widget()

        self._layout.addStretch()
        self._layout.addLayout(question_layout)
        self._layout.addStretch()
        self._layout.addWidget(self._plot_widget)
        self._layout.addStretch()
        self.setLayout(self._layout)

    def _get_question_layout(self) -> QVBoxLayout:
        question_layout = QVBoxLayout()
        question_layout.setContentsMargins(5, 25, 5, 5)

        question_label = LabelFactory.get_label_component(text=self._step.question, label_type=TextType.BIG_TITLE,
                                                          need_word_wrap=True, align=Qt.AlignHCenter)
        question_layout.addWidget(question_label, alignment=Qt.AlignHCenter)

        if self._need_help_data:
            help_button_layout = self._get_help_button_layout()
            question_layout.addLayout(help_button_layout)

        question_layout.addSpacing(20)

        self._bottom_buttons_layout = self._get_function_expression_buttons_layout()
        question_layout.addLayout(self._bottom_buttons_layout)

        self._help_text = LabelFactory.get_label_component(
            text='', label_type=TextType.SUBTITLE, align=Qt.AlignHCenter, need_word_wrap=True, set_visible=False
        )
        question_layout.addWidget(self._help_text)
        question_layout.addSpacing(25)

        continue_buttons_layout = self._get_continue_buttons_layout()
        question_layout.addLayout(continue_buttons_layout)
        question_layout.addStretch()

        return question_layout

    def _get_function_expression_buttons_layout(self) -> QHBoxLayout:
        layout = QHBoxLayout()
        layout.addStretch()
        options = self._get_options_to_display()
        for index, option in enumerate(options):
            graph_button = self._get_graph_button(index=index, option=option)
            layout.addWidget(graph_button)
            self._graph_buttons.append(graph_button)
            layout.addStretch()
        return layout

    def _get_graph_button(self, index: int, option: str) -> QPushButton:
        return ButtonFactory.get_button_component(
            title=option, minimum_width=90, minimum_height=90, text_size=22,
            function_to_connect=lambda val=index: self._validate_exercise(button_index=index),
        )

    def _get_continue_buttons_layout(self) -> QHBoxLayout:
        continue_layout = QHBoxLayout()

        icon = IconFactory.get_icon_widget(image_name='continue_button.png')
        self._continue_button = ButtonFactory.get_button_component(
            title='', function_to_connect=lambda: self._send_continue_signal(), icon=icon, icon_size=85,
            tooltip='Continuar', is_disable=True)

        icon = IconFactory.get_icon_widget(image_name='back_2_button.png')
        self._back_button = ButtonFactory.get_button_component(
            title='', function_to_connect=lambda: self._send_back_signal(), icon=icon, icon_size=85,
            tooltip='Ir al ejercicio anterior', is_disable=True)

        if self._exercise.exercise_order != 0 or self._step.order != 0:
            self._back_button.setDisabled(False)

        continue_layout.addStretch()
        continue_layout.addWidget(self._back_button)
        continue_layout.addStretch()
        continue_layout.addStretch()
        continue_layout.addWidget(self._continue_button)
        continue_layout.addStretch()
        return continue_layout

    def _set_plot_widget(self):
        function = self._get_function_to_draw()
        self._plot_widget = PlotFactory.get_plot([function], exercise=self._exercise, show_ends=False, show_grid=True)

    def _apply_resume(self):
        pressed_button = next(button for button in self._graph_buttons if button.text() == self._resume.response)
        correct_expression = self._get_correct_expression()
        self._set_graph(pressed_button=pressed_button, correct_expression=correct_expression,
                        is_answer_correct=pressed_button.text() == correct_expression)

    def _get_options_to_display(self):
        pass

    def _get_function_to_draw(self):
        pass

    def _get_correct_expression(self):
        pass

    def _get_error_function(self, expression: [str, None]):
        return None

    def _validate_exercise(self, button_index):
        pressed_button = self._graph_buttons[button_index]
        correct_expression = self._get_correct_expression()
        is_answer_correct = pressed_button.text() == correct_expression
        self._set_graph(pressed_button=pressed_button, correct_expression=correct_expression,
                        is_answer_correct=is_answer_correct)
        self._update_resume(pressed_button=pressed_button, is_answer_correct=is_answer_correct)

    def _set_graph(self, pressed_button: QPushButton, correct_expression: str, is_answer_correct: bool):
        border_color = '#2F8C53' if is_answer_correct else 'red'
        if not is_answer_correct:
            self._help_text.setText('Incorrecto.')
            correct_button = next(button for button in self._graph_buttons if button.text() == correct_expression)
            correct_button.setStyleSheet('background: #2F8C53; font-size: 22px')
            self._update_plot_with_error_data(pressed_button.text())
        else:
            self._help_text.setText('Correcto.')
        self._help_text.setVisible(True)
        self._help_text.setStyleSheet(f'color: {border_color}')

        for button in self._graph_buttons:
            button.setDisabled(True)

        pressed_button.setStyleSheet(f'background: {border_color}; font-size: 22px')
        self._continue_button.setStyleSheet(f'background: {border_color}')
        self._continue_button.setDisabled(False)

        if self._exercise.exercise_order != 0 or self._step.order != 0:
            self._back_button.setDisabled(False)

    def _update_plot_with_error_data(self, expression: str):
        error_function = self._get_error_function(expression=expression)
        if error_function:
            PlotFactory.update_plot(plot_widget=self._plot_widget, functions_to_update=[error_function],
                                    rgb_tuple=(255, 0, 0), no_points=True)
            label_functions = [(self._get_function_to_draw(), 'white'), (error_function, 'red')]
            PlotFactory.add_function_labels(plot_widget=self._plot_widget,
                                            functions_to_labelling_with_color=label_functions)

    def _update_resume(self, pressed_button: QPushButton, is_answer_correct: bool):
        resume_state = ResumeState.success if is_answer_correct else ResumeState.error
        self._resume.resume_state = resume_state
        self._resume.response = pressed_button.text()
        self.resume_signal.emit(self._resume)

from abc import abstractmethod

import pyqtgraph
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout

from src.projectConf.factories import LabelFactory, ButtonFactory, IconFactory
from src.projectConf.models.enums import TextType
from .component import Component
from ..factories import PlotFactory2
from ..models import ExerciseResume, FunctionExercise, FunctionStep
from ..models.enums import ResumeState


class GraphInteractionComponent(Component):
    resume_signal = pyqtSignal(ExerciseResume)

    def __init__(self, exercise: FunctionExercise, step: FunctionStep, resume: ExerciseResume,
                 need_help_data: bool = False, show_main_function_limits: bool = False,
                 show_function_labels: bool = False, need_validate_button: bool = False):
        super(GraphInteractionComponent, self).__init__(
            exercise=exercise, step=step, resume=resume, need_help_data=need_help_data,
            show_main_function_limits=show_main_function_limits, show_function_labels=show_function_labels
        )

        self._plot_widget: pyqtgraph.PlotWidget = None  # noqa
        self._help_text: QLabel = None  # noqa
        self._layout: QVBoxLayout = None  # noqa
        self._bottom_buttons_layout: QHBoxLayout = None  # noqa
        self._need_validate_button: bool = need_validate_button

    @abstractmethod
    def _get_correct_expression(self):
        pass

    @abstractmethod
    def _is_exercise_correct(self, expression_selected):
        pass

    @abstractmethod
    def _on_click_validation_button(self):
        pass

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

        question_layout.addSpacing(10)

        self._help_text = LabelFactory.get_label_component(
            text='', label_type=TextType.SUBTITLE, align=Qt.AlignHCenter, need_word_wrap=True, set_visible=False
        )
        question_layout.addWidget(self._help_text)

        if self._need_validate_button:
            self._setup_validate_button(layout=question_layout)
        question_layout.addSpacing(25)

        continue_buttons_layout = self._get_continue_buttons_layout()
        question_layout.addLayout(continue_buttons_layout)
        question_layout.addStretch()

        return question_layout

    def _setup_validate_button(self, layout: QVBoxLayout) -> None:
        validate_button = ButtonFactory.get_button_component(
            title='Comprobar ejercicio', minimum_width=90, minimum_height=90, text_size=22, tooltip='Validar',
            function_to_connect=lambda: self._on_click_validation_button()
        )
        layout.addWidget(validate_button, alignment=Qt.AlignHCenter)

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
        self._plot_widget = PlotFactory2.get_plot(function_range=self._exercise.exercise_domain)
        PlotFactory2.set_functions(graph=self._plot_widget, functions=[self._exercise.get_main_function()],
                                   function_width=5, color='white', show_limits=self._show_main_function_limits)

    def _apply_resume(self):
        expression_selected = self._resume.response
        self._validate_exercise(expression_selected=expression_selected, is_resume=True)

    def _validate_exercise(self, expression_selected, is_resume: bool = False):
        is_answer_correct = self._is_exercise_correct(expression_selected=expression_selected)
        if not is_resume:
            self._update_resume(expression_selected=expression_selected, is_answer_correct=is_answer_correct)

    def _update_resume(self, expression_selected: str, is_answer_correct: bool):
        resume_state = ResumeState.success if is_answer_correct else ResumeState.error
        self._resume.resume_state = resume_state
        self._resume.response = expression_selected
        self.resume_signal.emit(self._resume)

from abc import abstractmethod

import pyqtgraph
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy

from src.projectConf.factories import LabelFactory, ButtonFactory, IconFactory
from src.projectConf.models.enums import TextType
from ..component import Component
from ...factories import PlotFactory2
from ...models import ExerciseResume, FunctionExercise, FunctionStep
from ...models.enums import ResumeState


class GraphInteractionValidationComponent(Component):
    resume_signal = pyqtSignal(ExerciseResume)

    def __init__(self, exercise: FunctionExercise, step: FunctionStep, resume: ExerciseResume,
                 need_help_data: bool = False, show_main_function_limits: bool = False,
                 show_function_labels: bool = False):
        super(GraphInteractionValidationComponent, self).__init__(
            exercise=exercise, step=step, resume=resume, need_help_data=need_help_data,
            show_main_function_limits=show_main_function_limits, show_function_labels=show_function_labels
        )

        self._layout: QVBoxLayout = None  # noqa
        self._question_label: QLabel = None  # noqa
        self._help_text_label: QLabel = None  # noqa
        self._help_button: QPushButton = None  # noqa
        self._continue_button: QPushButton = None  # noqa
        self._back_button: QPushButton = None  # noqa
        self._plot_widget: pyqtgraph.PlotWidget = None  # noqa

    @abstractmethod
    def _get_correct_expression(self):
        pass

    def _setup_data(self):
        pass

    def _draw(self):
        self._layout = QHBoxLayout()
        self._setup_components()
        self._setup_layout()
        self.setLayout(self._layout)

    def _setup_components(self):
        self._question_label = self._get_question_label()
        self._help_button = self._get_help_button()
        # self._help_text_label = self._get_help_text()
        self._continue_button = self._get_continue_button()
        self._back_button = self._get_back_button()
        self._validate_button = self._get_validate_button()
        self._plot_widget = self._get_plot_widget()

    def _setup_layout(self):
        pass

    def _get_question_label(self) -> QLabel:
        return LabelFactory.get_label_component(text=self._step.question, label_type=TextType.BIG_TITLE,
                                                need_word_wrap=True, align=Qt.AlignHCenter)

    def _get_help_button(self) -> QPushButton:
        icon = IconFactory.get_icon_widget(image_name='help_button.png')
        return ButtonFactory.get_button_component(title='', function_to_connect=self._setup_help_data,
                                                  icon=icon, icon_size=45, tooltip='Ayuda')

    def _get_help_text(self) -> QLabel:
        return LabelFactory.get_label_component(text='Ayuda', label_type=TextType.NORMAL_TEXT,
                                                size_policy=(QSizePolicy.Fixed, QSizePolicy.Fixed))

    def _get_validate_button(self) -> QPushButton:
        return ButtonFactory.get_button_component(
            title='Comprobar ejercicio', minimum_width=90, minimum_height=90, text_size=22, tooltip='Validar',
            function_to_connect=lambda: self._on_click_validation_button()
        )

    @abstractmethod
    def _on_click_validation_button(self):
        pass

    def _get_continue_button(self) -> QPushButton:
        icon = IconFactory.get_icon_widget(image_name='continue_button.png')
        return ButtonFactory.get_button_component(
            title='', function_to_connect=lambda: self._send_continue_signal(), icon=icon, icon_size=85,
            tooltip='Continuar', is_disable=True
        )

    def _get_back_button(self) -> QPushButton:
        icon = IconFactory.get_icon_widget(image_name='back_2_button.png')
        back_button = ButtonFactory.get_button_component(
            title='', function_to_connect=lambda: self._send_back_signal(), icon=icon, icon_size=85,
            tooltip='Ir al ejercicio anterior', is_disable=True
        )

        if self._exercise.exercise_order != 0 or self._step.order != 0:
            back_button.setDisabled(False)

        return back_button

    def _get_plot_widget(self) -> pyqtgraph.PlotWidget:
        plot_widget = PlotFactory2.get_plot(function_range=self._exercise.exercise_domain)
        PlotFactory2.set_functions(graph=plot_widget, functions=[self._exercise.get_main_function()],
                                   function_width=5, color='white', show_limits=self._show_main_function_limits)
        return plot_widget

    @abstractmethod
    def _on_function_to_draw_click(self, plot_curve_item_selected, point_selected):
        pass

    def _apply_resume(self):
        expression_selected = self._resume.response
        self._validate_exercise(expression_selected=expression_selected, is_resume=True)

    def _validate_exercise(self, expression_selected, is_resume: bool = False):
        is_answer_correct = self._is_exercise_correct(expression_selected=expression_selected)
        if not is_resume:
            self._update_resume(expression_selected=expression_selected, is_answer_correct=is_answer_correct)

    @abstractmethod
    def _is_exercise_correct(self, expression_selected):
        pass

    def _update_resume(self, expression_selected: str, is_answer_correct: bool):
        resume_state = ResumeState.success if is_answer_correct else ResumeState.error
        self._resume.resume_state = resume_state
        self._resume.response = expression_selected
        self.resume_signal.emit(self._resume)

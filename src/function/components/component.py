from abc import abstractmethod

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy, QPushButton

from .help_data_components.help_data_dialog import HelpDataDialog
from ..models.enums.resume_state import ResumeState
from ..models.enums.step_type import StepType
from ..models.exercise_resume import ExerciseResume
from ..models.function_exercise import FunctionExercise
from ..models.function_step import FunctionStep
from ...projectConf.factories import ButtonFactory, LabelFactory
from ...projectConf.factories.icon_factory import IconFactory
from ...projectConf.models.enums.text_type import TextType


class Component(QWidget):
    continue_signal = pyqtSignal(StepType)
    back_signal = pyqtSignal(StepType)
    resume_signal = pyqtSignal(ExerciseResume)

    def __init__(self, exercise: FunctionExercise, step: FunctionStep, resume: ExerciseResume,
                 need_help_data: bool = False, show_main_function_limits: bool = False,
                 show_function_labels: bool = False):
        super(Component, self).__init__()

        self._exercise = exercise
        self._step = step
        self._resume = resume
        self._need_help_data = need_help_data
        self._show_main_function_limits = show_main_function_limits
        self._show_function_labels = show_function_labels

        self._help_button: QPushButton = None  # noqa
        self._info_button: QPushButton = None  # noqa

    def draw(self):
        self._setup_data()
        self._draw()
        self._setup_resume()

    @abstractmethod
    def _setup_data(self):
        pass

    @abstractmethod
    def _draw(self):
        pass

    def _setup_components(self):
        self._help_button = self._get_help_button()
        self._info_button = self._get_info_button()

    @abstractmethod
    def _apply_resume(self):
        pass

    @abstractmethod
    def _get_function_to_draw(self):
        pass

    def _setup_resume(self):
        if not self._resume:
            self._initialize_resume()
        elif self._resume.resume_state != ResumeState.pending:
            self._apply_resume()

        self.resume_signal.emit(self._resume)

    def _send_continue_signal(self):
        self.continue_signal.emit(self._step.type)

    def _send_back_signal(self):
        self.back_signal.emit(self._step.type)

    def _initialize_resume(self):
        self._resume = ExerciseResume(
            resume_state=ResumeState.pending, show_help=False, exercise_id=self._exercise.id,
            step_type=self._step.type, graph_expression=self._get_function_to_draw().expression, response=None
        )

    def _get_help_button(self) -> QPushButton:
        icon = IconFactory.get_icon_widget(image_name='question.png')
        return ButtonFactory.get_button_component(
            title='', function_to_connect=self._setup_help_data, secondary_button=True, icon=icon, icon_size=45,
            tooltip='Ayuda sobre el ejercicio'
        )

    def _get_info_button(self) -> QPushButton:
        icon = IconFactory.get_icon_widget(image_name='lessons.png')
        return ButtonFactory.get_button_component(
            title='', function_to_connect=self._setup_help_data, secondary_button=True, icon=icon, icon_size=45,
            tooltip='Ayuda sobre el concepto'
        )

    def _setup_help_data(self):
        help_data_dialog = HelpDataDialog(
            help_data_list=self._step.help_data_list, show_main_function_limits=self._show_main_function_limits,
            show_function_labels=self._show_function_labels
        )
        help_data_dialog.draw()

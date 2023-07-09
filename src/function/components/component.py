from abc import abstractmethod
from typing import List

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QPushButton

from .help_data_components.help_data_dialog import HelpDataDialog
from .video_component import VideoDialog
from ..models import Function
from ..models.enums.resume_state import ResumeState
from ..models.enums.step_type import StepType
from ..models.exercise_resume import ExerciseResume
from ..models.function_exercise import FunctionExercise
from ..models.function_step import FunctionStep
from ...projectConf.factories import ButtonFactory
from ...projectConf.factories.icon_factory import IconFactory


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

        self._video_dialog: VideoDialog = None  # noqa

        self._help_data_dialog: HelpDataDialog = None  # noqa

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
        if not self._need_help_data:
            self._info_button.setVisible(False)

    @abstractmethod
    def _apply_resume(self):
        pass

    @abstractmethod
    def _get_function_to_draw(self) -> [Function, List]:
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
        function = self._get_function_to_draw()[0] if isinstance(self._get_function_to_draw(), list) \
            else self._get_function_to_draw()
        self._resume = ExerciseResume(
            resume_state=ResumeState.pending, show_help=False, exercise_id=self._exercise.id,
            step_type=self._step.type, function_id=function.function_id, response=None
        )

    def _get_help_button(self) -> QPushButton:
        icon = IconFactory.get_icon_widget(image_name='question.png')
        return ButtonFactory.get_button_component(
            title='', function_to_connect=self._setup_question_data, secondary_button=True, icon=icon, icon_size=45,
            tooltip='Ayuda sobre el ejercicio'
        )

    def _setup_question_data(self):
        if not self._video_dialog:
            self._video_dialog = VideoDialog(step_info_data=self._step.step_info_data)
            self._video_dialog.close_signal.connect(self._set_video_dialog_close)
            self._video_dialog.draw()
            self._help_button.setDisabled(True)
            if self._info_button:
                self._info_button.setDisabled(True)

    def _set_video_dialog_close(self):
        if self._video_dialog:
            self._video_dialog.close()
            self._video_dialog = None
        if self._help_button:
            self._help_button.setDisabled(False)
        if self._info_button:
            self._info_button.setDisabled(False)

    def _get_info_button(self) -> QPushButton:
        icon = IconFactory.get_icon_widget(image_name='lessons.png')
        return ButtonFactory.get_button_component(
            title='', function_to_connect=self._setup_help_data, secondary_button=True, icon=icon, icon_size=45,
            tooltip='Ayuda sobre el concepto'
        )

    def _setup_help_data(self):
        if not self._help_data_dialog:
            self._help_data_dialog = HelpDataDialog(
                help_data_list=self._step.help_data_list, show_main_function_limits=self._show_main_function_limits,
                show_function_labels=self._show_function_labels
            )
            self._help_data_dialog.close_signal.connect(self._set_help_data_dialog_close)
            self._help_data_dialog.draw()
            self._info_button.setDisabled(True)
            if self._help_button:
                self._help_button.setDisabled(True)

    def _set_help_data_dialog_close(self):
        if self._help_button:
            self._help_button.setDisabled(False)
        self._help_data_dialog.close()
        self._help_data_dialog = None
        self._info_button.setDisabled(False)

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy

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

    label = 'Seleccionar la función.'

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

    def draw(self):
        self._setup_data()
        self._draw()
        self._setup_resume()

    def _setup_data(self):
        pass

    def _draw(self):
        pass

    def _setup_resume(self):
        if not self._resume:
            self._initialize_resume()
        elif self._resume.resume_state != ResumeState.pending:
            self._apply_resume()

    def _apply_resume(self):
        pass

    def _get_function_to_draw(self):
        pass

    def _send_continue_signal(self):
        self.continue_signal.emit(self._step.type)

    def _send_back_signal(self):
        self.back_signal.emit(self._step.type)

    def _initialize_resume(self):
        self._resume = ExerciseResume(
            resume_state=ResumeState.pending, show_help=False, exercise_id=self._exercise.id,
            step_type=self._step.type, graph_expression=self._get_function_to_draw().expression, response=None
        )
        self.resume_signal.emit(self._resume)

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

    def _setup_help_data(self):
        help_data_dialog = HelpDataDialog(
            help_data_list=self._step.help_data_list, show_main_function_limits=self._show_main_function_limits,
            show_function_labels=self._show_function_labels
        )
        help_data_dialog.draw()

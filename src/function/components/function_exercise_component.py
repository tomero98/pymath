from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout

from .bounded_range_component import BoundedRangeComponent
from .domain_indicate_component import DomainIndicateComponent
from .elementary_graph_component import ElementaryGraphComponent
from .elementary_shift_graph_component import ElementaryShiftGraphComponent
from .inverse_boolean_component import InverseBooleanComponent
from .inverse_delimited_component import InverseDelimitedComponent
from .inverse_selection_component import InverseSelectionComponent
from .maximum_minimum_component import MaximumMinimumComponent
from .root_domain_component import RootDomainComponent
from ..models.enums.step_type import StepType
from ..models.enums.resume_state import ResumeState
from ..models.exercise_resume import ExerciseResume
from ..models.function_exercise import FunctionExercise
from ..models.function_step import FunctionStep


class FunctionExerciseComponent(QWidget):
    continue_signal = pyqtSignal(ExerciseResume)
    back_exercise_signal = pyqtSignal(ExerciseResume)
    resume_signal = pyqtSignal(dict)
    exercise_finished_signal = pyqtSignal()

    def  __init__(self, exercise: FunctionExercise, need_help_data: bool = False, step_type: StepType = None,
                 resume_by_exercise_step_id: dict = {}):
        super(FunctionExerciseComponent, self).__init__()
        self._exercise = exercise

        self._current_step_component = None
        self._step_component_layout: QHBoxLayout = None
        self._title = None
        self._help_button = None
        self._resume_by_exercise_step_id = resume_by_exercise_step_id
        self._start_step_type = step_type

        self._draw(need_help_data=need_help_data)
        self._need_help_data = need_help_data

    def _draw(self, need_help_data: bool = False):
        layout = QVBoxLayout()
        self._step_component_layout = self._get_first_step_component_layout(need_help_data=need_help_data)

        layout.addLayout(self._step_component_layout)
        self.setLayout(layout)

    def _get_first_step_component_layout(self, need_help_data: bool = False) -> QHBoxLayout:
        layout = QHBoxLayout()
        self._current_step_component = self._get_first_step_component(need_help_data)
        layout.addWidget(self._current_step_component)
        return layout

    def _get_first_step_component(self, need_help_data: bool):
        try:
            first_step = self._exercise.steps[0] if not self._start_step_type \
                else next(step for step in self._exercise.steps if step.type == self._start_step_type)
            first_step_component = self._get_step_component(step=first_step, need_help_data=need_help_data)
            return first_step_component
        except IndexError:
            print('No hay más ejercicios jeje 2')
            exit(0)

    def _get_step_component(self, step: FunctionStep, need_help_data: bool = False):
        resume = self._get_current_step_resume(step=step, need_help_data=need_help_data)
        if step.type == StepType.boolean_inverse_exercise:
            component = InverseBooleanComponent(exercise=self._exercise, step=step)
        elif step.type == StepType.selection_inverse_exercise:
            component = InverseSelectionComponent(exercise=self._exercise, step=step)
        elif step.type == StepType.delimited_inverse_exercise:
            component = InverseDelimitedComponent(exercise=self._exercise, step=step)
        elif step.type in [StepType.indicate_domain_exercise, StepType.indicate_range_exercise]:
            component = DomainIndicateComponent(exercise=self._exercise, step=step)
        elif step.type == StepType.indicate_bounded_range_exercise:
            component = BoundedRangeComponent(exercise=self._exercise, step=step)
        elif step.type == StepType.indicate_roots_exercise:
            component = RootDomainComponent(exercise=self._exercise, step=step)
        elif step.type == StepType.indicate_elementary_exercise:
            component = ElementaryGraphComponent(exercise=self._exercise, step=step, resume=resume)
        elif step.type == StepType.indicate_elementary_shift_exercise:
            component = ElementaryShiftGraphComponent(exercise=self._exercise, step=step, resume=resume)
        elif step.type == StepType.maximum_relative_exercise:
            component = MaximumMinimumComponent(exercise=self._exercise, step=step)
        elif step.type == StepType.maximum_absolute_exercise:
            component = MaximumMinimumComponent(exercise=self._exercise, step=step)
        elif step.type == StepType.minimum_relative_exercise:
            component = MaximumMinimumComponent(exercise=self._exercise, step=step)
        elif step.type == StepType.minimum_absolute_exercise:
            component = MaximumMinimumComponent(exercise=self._exercise, step=step)
        component.continue_signal.connect(self._setup_next_step_component)
        component.back_signal.connect(self._setup_back_step_component)
        component.resume_signal.connect(self._setup_resume)

        self.resume_signal.emit(self._resume_by_exercise_step_id)
        return component

    def _get_current_step_resume(self, step: FunctionStep, need_help_data: bool):
        resume = self._resume_by_exercise_step_id.get((self._exercise.id, step.type))
        if not resume:
            resume = ExerciseResume(
                resume_state=ResumeState.pending, show_help=need_help_data, exercise_id=self._exercise.id,
                step_type=step.type, graph_id=self._exercise.get_main_function().function_id, response=None
            )
            self._resume_by_exercise_step_id[(self._exercise.id, step.type)] = resume
        return resume

    def _setup_help_data(self):
        self._current_step_component.setup_help_data()
        self._help_button.setDisabled(True)

    def _send_continue_signal(self, resume: ExerciseResume):
        self.continue_signal.emit(resume)

    def _send_back_exercise_signal(self, resume: ExerciseResume):
        self.back_exercise_signal.emit(resume)

    def _setup_next_step_component(self, resume: ExerciseResume):
        try:
            current_step_order = next(step.order for step in self._exercise.steps if step.type == resume.step_type)
            next_step = self._exercise.steps[current_step_order + 1]
            self._setup_step_component(next_step=next_step)
        except IndexError:
            self._send_continue_signal(resume=resume)

    def _setup_back_step_component(self, resume: ExerciseResume):
        try:
            if len(self._exercise.steps) == 1:
                self._send_back_exercise_signal(resume=resume)
                return None

            current_step_order = next(step.order for step in self._exercise.steps if step.type == resume.step_type)
            next_step = self._exercise.steps[current_step_order - 1]
            self._setup_step_component(next_step=next_step)
        except IndexError:
            self._send_back_exercise_signal(resume=resume)

    def set_step_component_by_combobox(self, step_component):
        self._setup_step_component(step_component=step_component)

    def _setup_step_component(self, next_step: FunctionStep = None, step_component=None):
        self._step_component_layout.removeWidget(self._current_step_component)
        self._current_step_component.setParent(None)
        self._current_step_component = self._get_step_component(next_step) if not step_component else step_component
        self._step_component_layout.insertWidget(2, self._current_step_component)

    def _setup_resume(self, resume: ExerciseResume):
        self._resume_by_exercise_step_id[(resume.exercise_id, resume.step_type)] = resume
        self.resume_signal.emit(self._resume_by_exercise_step_id)

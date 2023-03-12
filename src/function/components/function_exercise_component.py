from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout

from .domain_components import RootDomainComponent, BoundedRangeComponent, DomainIndicateComponent
from .elementary_graph_components import ElementaryGraphComponent, ElementaryShiftGraphComponent
from .inverse_components import InverseDelimitedComponent, InverseSelectionComponent, InverseConceptComponent
from .maximum_minimum_components import MaximumMinimumComponent
from ..models import ExerciseResume, FunctionExercise, FunctionStep
from ..models.enums import StepType


class FunctionExerciseComponent(QWidget):
    continue_signal = pyqtSignal(int)
    back_exercise_signal = pyqtSignal(int)
    resume_signal = pyqtSignal(ExerciseResume)

    def __init__(self, exercise: FunctionExercise, need_help_data: bool = False, start_step: FunctionStep = None,
                 resume_by_exercise_id_step_id: dict = {}):
        super(FunctionExerciseComponent, self).__init__()
        self._exercise = exercise

        self._current_step_component = None
        self._step_component_layout: QHBoxLayout = None
        self._title = None
        self._help_button = None
        self._resume_by_exercise_id_step_id = resume_by_exercise_id_step_id
        self._start_step = start_step if start_step else self._exercise.steps[0]
        self._need_help_data = need_help_data

    def draw(self):
        layout = QVBoxLayout()
        self._step_component_layout = self._get_first_step_component_layout(need_help_data=self._need_help_data)

        layout.addLayout(self._step_component_layout)
        self.setLayout(layout)

    def _get_first_step_component_layout(self, need_help_data: bool = False) -> QHBoxLayout:
        layout = QHBoxLayout()
        self._current_step_component = self._get_first_step_component(need_help_data)
        layout.addWidget(self._current_step_component)
        self._current_step_component.draw()
        return layout

    def _get_first_step_component(self, need_help_data: bool):
        try:
            first_step_component = self._get_step_component(step=self._start_step, need_help_data=need_help_data)
            return first_step_component
        except IndexError:
            print('No hay más ejercicios jeje 2')
            exit(0)

    def _get_step_component(self, step: FunctionStep, need_help_data: bool = False):
        resume = self._get_step_resume(step=step)

        if step.type == StepType.inverse_concept_exercise:
            component = InverseConceptComponent(exercise=self._exercise, step=step, resume=resume, need_help_data=False)
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
            component = ElementaryShiftGraphComponent(exercise=self._exercise, step=step, resume=resume,
                                                      need_help_data=True)
        elif step.type == StepType.maximum_relative_exercise:
            component = MaximumMinimumComponent(exercise=self._exercise, step=step)
        elif step.type == StepType.maximum_absolute_exercise:
            component = MaximumMinimumComponent(exercise=self._exercise, step=step)
        elif step.type == StepType.minimum_relative_exercise:
            component = MaximumMinimumComponent(exercise=self._exercise, step=step)
        elif step.type == StepType.minimum_absolute_exercise:
            component = MaximumMinimumComponent(exercise=self._exercise, step=step)

        self._setup_signals(component=component)

        return component

    def _get_step_resume(self, step: FunctionStep):
        return self._resume_by_exercise_id_step_id.get((self._exercise.id, step.type))

    def _setup_signals(self, component):
        component.continue_signal.connect(self._setup_next_step_component)
        component.back_signal.connect(self._setup_back_step_component)
        component.resume_signal.connect(self._setup_resume)

    def _setup_help_data(self):
        self._current_step_component.setup_help_data()
        self._help_button.setDisabled(True)

    def _setup_next_step_component(self, step_type: StepType):
        try:
            current_step_order = next(step.order for step in self._exercise.steps if step.type == step_type)
            next_step = self._exercise.steps[current_step_order + 1]
            self._setup_step_component(next_step=next_step)
        except IndexError:
            self._send_continue_signal()

    def _setup_back_step_component(self, step_type: StepType):
        current_step_order = next(step.order for step in self._exercise.steps if step.type == step_type)
        if current_step_order == 0:
            self._send_back_exercise_signal()
        else:
            next_step = self._exercise.steps[current_step_order - 1]
            self._setup_step_component(next_step=next_step)

    def _send_continue_signal(self):
        self.continue_signal.emit(self._exercise.id)

    def _send_back_exercise_signal(self):
        self.back_exercise_signal.emit(self._exercise.id)

    def set_step_component_by_combobox(self, step_component):
        self._setup_step_component(step_component=step_component)

    def _setup_step_component(self, next_step: FunctionStep = None, step_component=None):
        self._step_component_layout.removeWidget(self._current_step_component)
        self._current_step_component.setParent(None)
        self._current_step_component = self._get_step_component(next_step) if not step_component else step_component
        self._step_component_layout.insertWidget(2, self._current_step_component)
        self._current_step_component.draw()

    def _setup_resume(self, resume: ExerciseResume):
        self.resume_signal.emit(resume)

    def update_resume_dict(self, resume_by_exercise_id_step_id: dict):
        self._resume_by_exercise_id_step_id = resume_by_exercise_id_step_id

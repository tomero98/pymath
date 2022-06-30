from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout

from .bounded_range_component import BoundedRangeComponent
from .domain_indicate_component import DomainIndicateComponent
from .elementary_graph_component import ElementaryGraphComponent
from .inverse_boolean_component import InverseBooleanComponent
from .inverse_delimited_component import InverseDelimitedComponent
from .inverse_selection_component import InverseSelectionComponent
from .maximum_minimum_component import MaximumMinimumComponent
from ..models.enums.inverse_step_type import InverseStepType
from ..models.function_exercise import FunctionExercise
from ..models.function_step import FunctionStep
from ...projectConf.factories import ButtonFactory
from ...projectConf.factories.icon_factory import IconFactory


class FunctionExerciseComponent(QWidget):
    continue_signal = pyqtSignal()

    def __init__(self, exercise: FunctionExercise, need_help_data: bool = False):
        super(FunctionExerciseComponent, self).__init__()
        self._exercise = exercise

        self._current_step_component = None
        self._step_component_layout: QHBoxLayout = None
        self._title = None
        self._help_button = None

        self._next_step = self._get_next_step()
        self._draw(need_help_data=need_help_data)
        self._need_help_data = need_help_data

    def _get_next_step(self) -> FunctionStep:
        for step in self._exercise.steps:
            yield step

    def _draw(self, need_help_data: bool = False):
        layout = QVBoxLayout()
        self._step_component_layout = self._get_step_component_layout(need_help_data=need_help_data)

        layout.addLayout(self._step_component_layout)
        self.setLayout(layout)

    def _get_step_component_layout(self, need_help_data: bool = False) -> QHBoxLayout:
        layout = QHBoxLayout()
        layout.addStretch()
        layout.addSpacing(80)
        self._current_step_component = self._get_step_component()
        layout.addWidget(self._current_step_component)
        if need_help_data:
            help_layout = QVBoxLayout()
            icon = IconFactory.get_icon_widget(image_name='help_button.png')
            self._help_button = ButtonFactory.get_button_component(title='', function_to_connect=self._setup_help_data,
                                                                   icon=icon, icon_size=40, tooltip='Iniciar')
            help_layout.addSpacing(65)
            help_layout.addWidget(self._help_button, alignment=Qt.AlignTop)
            layout.addLayout(help_layout)
            layout.addStretch()
            self._current_step_component.validate_signal.connect(lambda: self._help_button.setDisabled(True))
        else:
            layout.addStretch()
        return layout

    def _get_step_component(self):
        try:
            next_step = next(self._next_step)
        except StopIteration:
            print('No hay más ejercicios jeje 2')
            exit(0)
        next_step_component = self._get_next_step_component(step=next_step)
        return next_step_component

    def _get_next_step_component(self, step: FunctionStep):
        if step.type == InverseStepType.boolean_inverse_exercise:
            component = InverseBooleanComponent(exercise=self._exercise, step=step)
        elif step.type == InverseStepType.selection_inverse_exercise:
            component = InverseSelectionComponent(exercise=self._exercise, step=step)
        elif step.type == InverseStepType.delimited_inverse_exercise:
            component = InverseDelimitedComponent(exercise=self._exercise, step=step)
        elif step.type == InverseStepType.indicate_domain_exercise:
            component = DomainIndicateComponent(exercise=self._exercise, step=step)
        elif step.type == InverseStepType.indicate_bounded_range_exercise:
            component = BoundedRangeComponent(exercise=self._exercise, step=step)
        elif step.type == InverseStepType.indicate_elementary_exercise:
            component = ElementaryGraphComponent(exercise=self._exercise, step=step)
        elif step.type == InverseStepType.maximum_relative_exercise:
            component = MaximumMinimumComponent(exercise=self._exercise, step=step)
        elif step.type == InverseStepType.maximum_absolute_exercise:
            component = MaximumMinimumComponent(exercise=self._exercise, step=step)
        elif step.type == InverseStepType.minimum_relative_exercise:
            component = MaximumMinimumComponent(exercise=self._exercise, step=step)
        elif step.type == InverseStepType.minimum_absolute_exercise:
            component = MaximumMinimumComponent(exercise=self._exercise, step=step)
        component.continue_signal.connect(self._setup_next_step_component)
        return component

    def _setup_help_data(self):
        self._current_step_component.setup_help_data()
        self._help_button.setDisabled(True)

    def _send_continue_signal(self):
        self.continue_signal.emit()

    def _setup_next_step_component(self, is_correct_answer: bool):
        try:
            next_step: FunctionStep = next(self._next_step)
            self._step_component_layout.removeWidget(self._current_step_component)
            self._current_step_component.setParent(None)
            self._current_step_component = self._get_next_step_component(next_step)
            self._step_component_layout.insertWidget(2, self._current_step_component)
            if self._help_button:
                self._help_button.setDisabled(False)
            if self._need_help_data:
                self._current_step_component.validate_signal.connect(lambda: self._help_button.setDisabled(True))
        except StopIteration:
            self._send_continue_signal()

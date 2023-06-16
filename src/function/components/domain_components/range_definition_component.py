from PyQt5.QtCore import pyqtSignal

from . import DomainDefinitionComponent
from ...models import FunctionExercise, FunctionStep, ExerciseResume


class RangeDefinitionComponent(DomainDefinitionComponent):
    continue_signal = pyqtSignal(bool)
    label = 'Indicar el rango de la función'
    _ORIENTATION = 'horizontal'

    def __init__(self, exercise: FunctionExercise, step: FunctionStep, resume: ExerciseResume,
                 need_help_data: bool = False):
        super(RangeDefinitionComponent, self).__init__(
            exercise=exercise, step=step, resume=resume, need_help_data=need_help_data
        )

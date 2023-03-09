from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget

from ..models.enums.resume_state import ResumeState
from ..models.enums.step_type import StepType
from ..models.exercise_resume import ExerciseResume
from ..models.function_exercise import FunctionExercise
from ..models.function_step import FunctionStep


class Component(QWidget):
    continue_signal = pyqtSignal(StepType)
    back_signal = pyqtSignal(StepType)
    resume_signal = pyqtSignal(ExerciseResume)

    label = 'Seleccionar la función.'

    def __init__(self, exercise: FunctionExercise, step: FunctionStep, resume: ExerciseResume):
        super(Component, self).__init__()

        self._exercise = exercise
        self._step = step
        self._resume = resume

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

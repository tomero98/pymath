from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget

from ..models.exercise_resume import ExerciseResume


class Component(QWidget):
    continue_signal = pyqtSignal(ExerciseResume)
    back_signal = pyqtSignal(ExerciseResume)
    resume_signal = pyqtSignal(ExerciseResume)

    label = 'Seleccionar la función.'

    def __init__(self):
        super(Component, self).__init__()

    def _send_continue_signal(self):
        self.continue_signal.emit(self._resume)

    def _send_back_signal(self):
        self.back_signal.emit(self._resume)

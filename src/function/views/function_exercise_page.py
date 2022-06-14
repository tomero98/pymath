import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QPushButton

from src.function.components.function_exercise_component import FunctionExerciseComponent
from src.function.data_mappers.function_exercise_data_mapper import FunctionExerciseDataMapper
from src.function.models.function_exercise import FunctionExercise
from src.projectConf.components import Window
from src.projectConf.models import Topic


class FunctionExercisePage(Window):
    def __init__(self, subtopic: Topic):
        title = subtopic.title
        super(FunctionExercisePage, self).__init__(title=title)

        self.subtopic = subtopic
        self._exercises = []
        self._layout = None
        self._current_exercise_component = None
        self._get_exercise_data(subtopic_id=subtopic.id)
        self._next_exercise = self._get_next_exercise()

    def _get_exercise_data(self, subtopic_id: int):
        self._exercises = FunctionExerciseDataMapper.get_function_exercise(topic_id=subtopic_id)

    def _get_next_exercise(self):
        for exercise in self._exercises:
            yield exercise

    def draw(self, *args, **kwargs):
        main_window = QWidget()
        self._layout = QVBoxLayout()

        self._current_exercise_component = self._get_current_exercise_component()
        self._set_layout()

        main_window.setLayout(self._layout)
        self.setCentralWidget(main_window)
        self.show()

    def _get_current_exercise_component(self):
        try:
            current_exercise: FunctionExercise = next(self._next_exercise)
            current_component = FunctionExerciseComponent(exercise=current_exercise, need_help_data=True)
            current_component.continue_signal.connect(self._setup_next_exercise)
            return current_component
        except StopIteration:
            print('No hay ejercicios de este tipo')
            sys.exit(0)

    @staticmethod
    def _get_continue_button_widget():
        return QPushButton('Continue')

    def _set_layout(self):
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self._layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self._layout.addWidget(self._current_exercise_component)

    def keyPressEvent(self, e):
        if e.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.continue_signal.emit()
        elif e.key() == Qt.Key_Escape:
            self.close_signal.emit()

    def _setup_next_exercise(self):
        try:
            next_exercise: FunctionExercise = next(self._next_exercise)
            self._layout.removeWidget(self._current_exercise_component)
            self._current_exercise_component.setParent(None)
            self._current_exercise_component = FunctionExerciseComponent(exercise=next_exercise)
            self._current_exercise_component.continue_signal.connect(self._setup_next_exercise)
            self._layout.addWidget(self._current_exercise_component)
        except StopIteration:
            print('No hay más ejercicios jeje')
            exit(0)

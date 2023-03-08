import random
import sys

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QComboBox

from src.function.components.function_exercise_component import FunctionExerciseComponent
from src.function.data_mappers.function_exercise_data_mapper import FunctionExerciseDataMapper
from src.function.models.enums.inverse_exercise_type import FunctionExerciseType
from src.function.models.enums.step_type import StepType
from src.function.models.exercise_resume import ExerciseResume
from src.function.models.function_exercise import FunctionExercise
from src.projectConf.components import Window
from src.projectConf.factories import ButtonFactory, LabelFactory
from src.projectConf.factories.dialog_factory import DialogFactory
from src.projectConf.factories.icon_factory import IconFactory
from src.projectConf.models import Topic
from src.projectConf.models.enums.text_type import TextType


class FunctionExercisePage(Window):
    back_signal = pyqtSignal()

    def __init__(self, topic: Topic):
        super(FunctionExercisePage, self).__init__(title=topic.title)

        self._topic = topic
        self._exercises: List[FunctionExercise] = []  # noqa
        self._steps_done = []
        self._step_widget_by_label = {}
        self._resume_by_exercise_step_id = {}

        self._layout: QVBoxLayout = None  # noqa
        self._steps_done_widget: QComboBox = None  # noqa
        self._header_layout = None
        self._current_exercise_component = None

        self._get_exercise_data(topic_id=topic.id)

    def _get_exercise_data(self, topic_id: int):
        # TODO CUSTOM NUM EXERCISES
        self._exercises = FunctionExerciseDataMapper.get_function_exercise(topic_id=topic_id)

    def draw(self, *args, **kwargs):
        main_window = QWidget()
        self._layout = QVBoxLayout()

        self._header_layout = self._get_header_layout()

        self._combobox_layout = self._get_combobox_layout()

        self._current_exercise_component = self._get_first_exercise_component()
        self._save_step()
        self._set_layout()

        main_window.setLayout(self._layout)
        self.setCentralWidget(main_window)
        self.show()

    def _get_header_layout(self) -> QHBoxLayout:
        header_layout = QHBoxLayout()

        back_button = self._get_back_button()
        breadcrumb_layout = self._get_breadcrumb_layout()

        header_layout.addWidget(back_button)
        header_layout.addStretch()
        header_layout.addLayout(breadcrumb_layout)
        header_layout.addStretch()
        return header_layout

    def _get_back_button(self) -> QPushButton:
        icon = IconFactory.get_icon_widget(image_name='back_button.png')
        back_button = ButtonFactory.get_button_component(title='', function_to_connect=self._show_dialog, icon=icon,
                                                         icon_size=30, tooltip='Atrás')
        return back_button

    def _get_breadcrumb_layout(self) -> QHBoxLayout:
        breadcrumb_layout = QHBoxLayout()

        function_label = LabelFactory.get_label_component(text='Funciones', label_type=TextType.NORMAL_TEXT,
                                                          set_underline=True, set_cursive=True)
        arrow_label = LabelFactory.get_label_image_component(image_name='breadcrumb_arrow.png', width=10, height=10)
        exercise_label = LabelFactory.get_label_component(text=self._topic.title, label_type=TextType.NORMAL_TEXT,
                                                          set_underline=True, set_cursive=True)

        breadcrumb_layout.addWidget(function_label)
        breadcrumb_layout.addSpacing(5)
        breadcrumb_layout.addWidget(arrow_label)
        breadcrumb_layout.addSpacing(5)
        breadcrumb_layout.addWidget(exercise_label)
        return breadcrumb_layout

    def _get_combobox_layout(self) -> QHBoxLayout:
        combobox_layout = QHBoxLayout()
        self._steps_done_widget = QComboBox()
        self._steps_done_widget.addItem('')
        self._steps_done_widget.setDisabled(True)
        combobox_label = LabelFactory.get_label_component(text='Ejercicio actual:', label_type=TextType.NORMAL_TEXT,
                                                          set_underline=True)
        combobox_layout.addStretch()
        combobox_layout.addWidget(combobox_label)
        combobox_layout.addSpacing(10)
        combobox_layout.addWidget(self._steps_done_widget)
        combobox_layout.addStretch()

        self._steps_done_widget.activated.connect(self._update_step_component)
        return combobox_layout

    def _get_first_exercise_component(self):
        try:
            first_exercise = self._exercises[0]
            need_help_data = True
            current_component = FunctionExerciseComponent(exercise=first_exercise, need_help_data=need_help_data,
                                                          resume_by_exercise_step_id=self._resume_by_exercise_step_id)
            current_component.continue_signal.connect(self._setup_next_exercise)
            current_component.back_exercise_signal.connect(self._setup_back_exercise)
            current_component.resume_signal.connect(self._setup_resume)
            current_component.exercise_finished_signal.connect(self._save_step)
            return current_component
        except IndexError:
            print('No hay ejercicios de este tipo')
            sys.exit(0)

    def _set_layout(self):
        self._layout.setContentsMargins(10, 5, 0, 0)
        self._layout.setSpacing(0)
        self._layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self._layout.addLayout(self._header_layout)
        self._layout.addSpacing(10)
        self._layout.addLayout(self._combobox_layout)
        self._layout.addWidget(self._current_exercise_component)

    def keyPressEvent(self, e):
        if e.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.continue_signal.emit()
        elif e.key() == Qt.Key_Escape:
            self._show_exit_dialog()

    def _show_dialog(self):
        self._dialog_widget = DialogFactory.get_dialog_widget(
            text='¿Quieres volver a atrás?', accepted_fn=self._back_signal, rejected_fn=self._close_dialog
        )
        self._dialog_widget.exec()

    def _back_signal(self):
        self.back_signal.emit()
        self._dialog_widget.close()

    def _close_dialog(self):
        self._dialog_widget.close()

    def _setup_next_exercise(self, resume: ExerciseResume):
        try:
            current_exercise_order = next(
                exercise.exercise_order for exercise in self._exercises if exercise.id == resume.exercise_id
            )
            next_exercise = self._exercises[current_exercise_order + 1]

            self._set_exercise_component(next_exercise=next_exercise)
        except:
            self.back_signal.emit()

    def _setup_back_exercise(self, resume: ExerciseResume):
        try:
            current_exercise_order = next(
                exercise.exercise_order for exercise in self._exercises if exercise.id == resume.exercise_id
            )
            next_exercise = self._exercises[current_exercise_order - 1]

            self._set_exercise_component(next_exercise=next_exercise, step_type=next_exercise.steps[-1].type)
        except:
            self.back_signal.emit()

    def _set_exercise_component(self, next_exercise: FunctionExercise, step_type: StepType = None):
        self._layout.removeWidget(self._current_exercise_component)
        self._current_exercise_component.setParent(None)
        self._current_exercise_component = FunctionExerciseComponent(
            exercise=next_exercise, step_type=step_type, resume_by_exercise_step_id=self._resume_by_exercise_step_id
        )
        self._current_exercise_component.continue_signal.connect(self._setup_next_exercise)
        self._current_exercise_component.back_exercise_signal.connect(self._setup_back_exercise)
        self._current_exercise_component.resume_signal.connect(self._setup_resume)
        self._current_exercise_component.exercise_finished_signal.connect(self._save_step)
        self._layout.addWidget(self._current_exercise_component)

    def _show_exit_dialog(self):
        self._exit_dialog_widget = DialogFactory.get_dialog_widget(
            text='¿Quieres salir de la aplicación?', accepted_fn=self._exit_signal, rejected_fn=self._no_exit_dialog
        )
        self._exit_dialog_widget.exec()

    def _exit_signal(self):
        self._exit_dialog_widget.close()
        exit(0)

    def _no_exit_dialog(self):
        self._exit_dialog_widget.close()

    def _save_step(self):
        step = self._current_exercise_component._current_step_component
        step_label = f'Ejercicio: {step.label}'

        if step_label in self._step_widget_by_label:
            return None

        self._steps_done_widget.addItem(step_label)
        self._steps_done_widget.adjustSize()
        self._steps_done_widget.setCurrentIndex(self._steps_done_widget.count() - 1)
        self._step_widget_by_label[step_label] = None

        if self._steps_done_widget.count() < 2:
            self._steps_done_widget.setDisabled(True)
        else:
            self._steps_done_widget.setDisabled(False)

    def _update_step_component(self):
        current_text_label = self._steps_done_widget.currentText()
        step_component = self._step_widget_by_label[current_text_label]
        self._current_exercise_component.set_step_component_by_combobox(step_component)

    def _setup_resume(self, resume_by_exercise_step_id: dict):
        self._resume_by_exercise_step_id = resume_by_exercise_step_id

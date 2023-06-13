import sys

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QComboBox

from src.function.components.function_exercise_component import FunctionExerciseComponent
from src.function.data_mappers.function_exercise_data_mapper import FunctionExerciseDataMapper
from src.function.models.exercise_resume import ExerciseResume
from src.function.models.function_exercise import FunctionExercise
from src.function.models.function_step import FunctionStep
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
        self._resume_by_exercise_id_step_id = {}

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

        self._setup_first_exercise_component()
        self._set_layout()

        main_window.setLayout(self._layout)
        self.setCentralWidget(main_window)
        self.show()

    def _get_header_layout(self) -> QHBoxLayout:
        header_layout = QHBoxLayout()

        back_button = self._get_back_button()
        self._combobox_layout = self._get_combobox_layout()
        next_button = self._get_next_button()

        header_layout.addSpacing(50)
        header_layout.addWidget(back_button)
        header_layout.addStretch()
        header_layout.addLayout(self._combobox_layout)
        header_layout.addStretch()
        header_layout.addWidget(next_button)
        header_layout.addSpacing(50)
        return header_layout

    def _get_back_button(self) -> QPushButton:
        icon = IconFactory.get_icon_widget(image_name='left-arrow.png')
        back_button = ButtonFactory.get_button_component(
            title='', function_to_connect=self._setup_previous_exercise, icon=icon, icon_size=35,
            tooltip='Ejercicio anterior', secondary_button=True
        )
        return back_button

    def _setup_previous_exercise(self):
        print(1)

    def _get_next_button(self) -> QPushButton:
        icon = IconFactory.get_icon_widget(image_name='arrow-right.png')
        back_button = ButtonFactory.get_button_component(
            title='', function_to_connect=self._setup_next_exercise2, icon=icon, icon_size=35,
            tooltip='Siguiente ejercicio', secondary_button=True)
        return back_button

    def _setup_next_exercise2(self):
        print(1)

    def _get_combobox_layout(self) -> QHBoxLayout:
        combobox_layout = QHBoxLayout()
        self._steps_done_widget = QComboBox()
        self._steps_done_widget.setStyleSheet('background-color: #CBC5F8;')
        self._steps_done_widget.setDisabled(True)
        combobox_label = LabelFactory.get_label_component(text='Ejercicio actual:', label_type=TextType.SUBTITLE)
        combobox_layout.addStretch()
        combobox_layout.addWidget(combobox_label, alignment=Qt.AlignVCenter)
        combobox_layout.addSpacing(15)
        combobox_layout.addWidget(self._steps_done_widget)
        combobox_layout.addStretch()

        self._steps_done_widget.activated.connect(self._update_step_component)
        return combobox_layout

    def _setup_first_exercise_component(self):
        try:
            first_exercise = self._exercises[0]
            need_help_data = True
            self._current_exercise_component = FunctionExerciseComponent(
                exercise=first_exercise, need_help_data=need_help_data,
                resume_by_exercise_id_step_id=self._resume_by_exercise_id_step_id
            )

            self._setup_signals(component=self._current_exercise_component)
            self._current_exercise_component.draw()
        except IndexError:
            print('No hay ejercicios de este tipo')
            sys.exit(0)

    def _setup_signals(self, component) -> None:
        component.continue_signal.connect(self._setup_next_exercise)
        component.back_exercise_signal.connect(self._setup_back_exercise)
        component.resume_signal.connect(self._setup_resume)

    def _set_layout(self):
        self._layout.setContentsMargins(10, 35, 10, 0)
        self._layout.setSpacing(0)
        self._layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self._layout.addLayout(self._header_layout)
        self._layout.addSpacing(10)
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

    def _setup_next_exercise(self, current_exercise_id: int):
        try:
            current_exercise_order = next(
                exercise.exercise_order for exercise in self._exercises if exercise.id == current_exercise_id
            )
            next_exercise = self._exercises[current_exercise_order + 1]
            self._set_exercise_component(next_exercise=next_exercise)
        except:
            self.back_signal.emit()

    def _setup_back_exercise(self, current_exercise_id: int):
        current_exercise_order = next(
            exercise.exercise_order for exercise in self._exercises if exercise.id == current_exercise_id
        )
        next_exercise = self._exercises[current_exercise_order - 1]
        self._set_exercise_component(next_exercise=next_exercise, start_step=next_exercise.steps[-1])

    def _set_exercise_component(self, next_exercise: FunctionExercise, start_step: FunctionStep = None):
        self._layout.removeWidget(self._current_exercise_component)
        self._current_exercise_component.setParent(None)
        self._current_exercise_component = FunctionExerciseComponent(
            exercise=next_exercise, start_step=start_step,
            resume_by_exercise_id_step_id=self._resume_by_exercise_id_step_id
        )

        self._setup_signals(component=self._current_exercise_component)
        self._current_exercise_component.draw()
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

    def _update_step_component(self, *args, **kwargs):
        current_text_label = self._steps_done_widget.currentText()
        # TODO: create a dict key (exercise_id, step) by label and update method set_step_component
        # self._current_exercise_component.set_step_component_by_combobox(step_component)

    def _setup_resume(self, resume: ExerciseResume):
        key = (resume.exercise_id, resume.step_type)
        if key not in self._resume_by_exercise_id_step_id:
            self._save_step_in_steps_done_widget(resume=resume)
        self._resume_by_exercise_id_step_id[key] = resume
        self._current_exercise_component.update_resume_dict(
            resume_by_exercise_id_step_id=self._resume_by_exercise_id_step_id
        )

    def _save_step_in_steps_done_widget(self, resume: ExerciseResume):
        current_exercise = next(exercise for exercise in self._exercises if exercise.id == resume.exercise_id)
        step = self._current_exercise_component._current_step_component
        step_label = f'Ejercicio {current_exercise.exercise_order + 1}: {step.label}'

        self._steps_done_widget.addItem(step_label)
        self._steps_done_widget.adjustSize()
        self._steps_done_widget.setCurrentIndex(self._steps_done_widget.count() - 1)
        self._steps_done_widget.setDisabled(self._steps_done_widget.count() < 2)

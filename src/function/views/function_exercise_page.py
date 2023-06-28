import sys
from copy import deepcopy

from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QComboBox, QGraphicsDropShadowEffect

from src.function.components.function_exercise_component import FunctionExerciseComponent
from src.function.data_mappers import ExerciseResumeDataMapper
from src.function.data_mappers.function_exercise_data_mapper import FunctionExerciseDataMapper
from src.function.models.enums import ResumeState
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

        self._topic: Topic = topic
        self._exercises: List[FunctionExercise] = []  # noqa
        self._resume_by_exercise_id_step_id: dict = {}
        self._exercise_step_type_by_label: dict = {}

        self._layout: QVBoxLayout = None  # noqa
        self._steps_done_widget: QComboBox = None  # noqa
        self._header_layout: QHBoxLayout = None  # noqa
        self._current_exercise_component: FunctionExerciseComponent = None  # noqa
        self._next_button: QPushButton = None  # noqa
        self._back_button: QPushButton = None  # noqa
        self._header_widget: QWidget = None  # noqa
        self._get_exercise_data()

    def _get_exercise_data(self):
        self._exercises = FunctionExerciseDataMapper.get_function_exercise(topic=self._topic)

    def draw(self, *args, **kwargs):
        main_window = QWidget()
        self._layout = QVBoxLayout()

        self._header_widget = self._get_header_layout()

        self._setup_first_exercise_component()
        self._set_layout()

        main_window.setLayout(self._layout)
        self.setCentralWidget(main_window)
        self.show()

    def _get_header_layout(self) -> QWidget:
        header = QWidget()
        header_layout = QHBoxLayout()

        self._back_button = self._get_back_button()
        self._combobox_layout = self._get_combobox_layout()
        self._next_button = self._get_next_button()

        header_layout.addSpacing(50)
        header_layout.addWidget(self._back_button)
        header_layout.addStretch()
        header_layout.addLayout(self._combobox_layout)
        header_layout.addStretch()
        header_layout.addWidget(self._next_button)
        header_layout.addSpacing(50)
        header.setLayout(header_layout)
        header.setObjectName('container')
        effect = QGraphicsDropShadowEffect()
        effect.setOffset(0, 0)
        effect.setBlurRadius(15)
        header.setGraphicsEffect(effect)
        header.setFixedSize(550, 100)
        header.setMinimumSize(QSize(header.minimumSizeHint().width() * 2, header.minimumSizeHint().height() * 1.2))
        header.setMaximumSize(QSize(header.minimumSizeHint().width() * 2, header.minimumSizeHint().height() * 1.2))
        return header

    def _get_back_button(self) -> QPushButton:
        icon = IconFactory.get_icon_widget(image_name='left-arrow.png')
        back_button = ButtonFactory.get_button_component(
            title='', function_to_connect=self._setup_previous_exercise, icon=icon, icon_size=35,
            tooltip='Ejercicio anterior', secondary_button=True, is_disable=True
        )
        return back_button

    def _setup_previous_exercise(self):
        self._current_exercise_component.setup_back_step_component()

    def _get_next_button(self) -> QPushButton:
        icon = IconFactory.get_icon_widget(image_name='arrow-right.png')
        next_button = ButtonFactory.get_button_component(
            title='', function_to_connect=self._setup_next_step, icon=icon, icon_size=35,
            tooltip='Siguiente ejercicio', secondary_button=True, is_disable=True)
        return next_button

    def _setup_next_step(self):
        self._current_exercise_component.setup_next_step_component()

    def _get_combobox_layout(self) -> QHBoxLayout:
        combobox_layout = QHBoxLayout()
        self._steps_done_widget = QComboBox()
        self._steps_done_widget.setStyleSheet('background-color: #ECDAC6;')
        self._steps_done_widget.setDisabled(True)
        combobox_label = LabelFactory.get_label_component(text='Ejercicio actual:', label_type=TextType.SUBTITLE,
                                                          set_bold=True)
        exercise_count_label = LabelFactory.get_label_component(text=f'/ {len(self._exercises)}',
                                                                label_type=TextType.SUBTITLE, set_bold=True)
        combobox_layout.addWidget(combobox_label, alignment=Qt.AlignVCenter)
        combobox_layout.addSpacing(15)
        combobox_layout.addWidget(self._steps_done_widget)
        combobox_layout.addSpacing(15)
        combobox_layout.addWidget(exercise_count_label, alignment=Qt.AlignVCenter)

        self._steps_done_widget.activated.connect(self._update_step_component)
        return combobox_layout

    def _setup_first_exercise_component(self):
        try:
            first_exercise = self._exercises[0]
            self._current_exercise_component = FunctionExerciseComponent(
                exercise=first_exercise, resume_by_exercise_id_step_id=self._resume_by_exercise_id_step_id
            )

            self._setup_signals(component=self._current_exercise_component)
            self._current_exercise_component.draw()
        except IndexError as e:
            print('No hay ejercicios de este tipo')
            sys.exit(0)

    def _setup_signals(self, component) -> None:
        component.continue_signal.connect(self._setup_next_exercise)
        component.back_exercise_signal.connect(self._setup_back_exercise)
        component.resume_signal.connect(self._setup_resume)

    def _set_layout(self):
        self._layout.setContentsMargins(0, 10, 0, 0)
        self._layout.setSpacing(0)
        self._layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self._layout.addWidget(self._header_widget, alignment=Qt.AlignHCenter)
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

    def _update_step_component(self):
        current_text_label = self._steps_done_widget.currentText()
        exercise, step = self._exercise_step_type_by_label[current_text_label]
        self._set_exercise_component(next_exercise=exercise, start_step=step)

    def _setup_resume(self, resume: ExerciseResume):
        key = (resume.exercise_id, resume.step_type)

        if key not in self._resume_by_exercise_id_step_id:
            self._save_step_in_steps_done_widget(resume=resume)
        else:
            previous_resume = self._resume_by_exercise_id_step_id[key]
            if previous_resume.resume_state == ResumeState.pending and resume.resume_state != ResumeState.pending:
                self._save_resume_in_db(resume=resume)

        self._resume_by_exercise_id_step_id[key] = deepcopy(resume)
        self._current_exercise_component.update_resume_dict(
            resume_by_exercise_id_step_id=self._resume_by_exercise_id_step_id
        )

        self._setup_save_widget_status(resume=resume)
        self._set_state_next_back_button(resume=resume)

    def _save_step_in_steps_done_widget(self, resume: ExerciseResume):
        current_exercise = next(exercise for exercise in self._exercises if exercise.id == resume.exercise_id)
        step = self._current_exercise_component._current_step_component  # noqa
        step_label = f'Ejercicio {current_exercise.exercise_order + 1}: {step.label}'

        self._exercise_step_type_by_label[step_label] = (current_exercise, step._step)  # noqa

        self._steps_done_widget.addItem(step_label)
        self._steps_done_widget.adjustSize()
        self._steps_done_widget.setCurrentIndex(self._steps_done_widget.count() - 1)
        self._steps_done_widget.setDisabled(self._steps_done_widget.count() < 2)

    def _save_resume_in_db(self, resume: ExerciseResume):
        ExerciseResumeDataMapper.save_resume_state(resume=resume)

    def _setup_save_widget_status(self, resume: ExerciseResume):
        current_exercise = next(exercise for exercise in self._exercises if exercise.id == resume.exercise_id)
        step = self._current_exercise_component._current_step_component  # noqa
        step_label = f'Ejercicio {current_exercise.exercise_order + 1}: {step.label}'
        for index in range(self._steps_done_widget.count()):
            text = self._steps_done_widget.itemText(index)
            if text == step_label:
                self._steps_done_widget.setCurrentIndex(index)
                break

    def _set_state_next_back_button(self, resume: ExerciseResume):
        current_exercise = next(exercise for exercise in self._exercises if exercise.id == resume.exercise_id)
        self._set_state_next_button(resume=resume, current_exercise=current_exercise)
        self._set_state_back_button(resume=resume, current_exercise=current_exercise)

    def _set_state_next_button(self, resume: ExerciseResume, current_exercise: FunctionExercise):
        if resume.resume_state == ResumeState.pending:
            self._next_button.setDisabled(True)
        else:
            self._next_button.setDisabled(False)

        is_last_exercise = self._exercises[-1] == current_exercise
        is_last_step = self._exercises[-1].steps[-1].type == resume.step_type
        is_last = is_last_exercise and is_last_step
        if not is_last:
            icon = IconFactory.get_icon_widget(image_name='arrow-right.png')
            self._next_button.setIcon(icon)
        else:
            icon = IconFactory.get_icon_widget(image_name='double-check.png')
            self._next_button.setIcon(icon)

    def _set_state_back_button(self, resume: ExerciseResume, current_exercise: FunctionExercise):
        is_first_exercise = self._exercises[0] == current_exercise
        is_first_step = self._exercises[0].steps[0].type == resume.step_type

        is_first = is_first_exercise and is_first_step
        if is_first:
            self._back_button.setDisabled(True)
        else:
            self._back_button.setDisabled(False)

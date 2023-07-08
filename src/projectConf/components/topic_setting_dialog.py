from collections import defaultdict
from copy import deepcopy
from typing import List

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QCheckBox, QHBoxLayout

from ..data_mappers import TopicDataMapper
from ..factories import ButtonFactory, LabelFactory, IconFactory
from ..models import Topic, ExerciseSetting, StepSetting
from ..models.enums import TextType
from ...function.models.enums import FunctionExerciseType


class TopicSettingDialog(QWidget):
    close_signal = pyqtSignal()

    def __init__(self, topic: Topic):
        super(TopicSettingDialog, self).__init__()

        self._topic: Topic = topic
        self._topic_edited: Topic = deepcopy(self._topic)
        self._checkbox_step_list_by_exercise_id: defaultdict = defaultdict(list)
        self._checkbox_exercise_list: List[QCheckBox] = []

        self._slider_label: QLabel = None  # noqa
        self._save_label: QLabel = None  # noqa

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.close_signal.emit()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close_signal.emit()

    def draw(self):
        self.setObjectName('application')
        self.setStyleSheet("""
                    QWidget#application {
                        background-color: #EDEDE9;
                    }"""
                           )
        self.setWindowTitle('Configuración del ejercicio')

        layout = QVBoxLayout()

        settings_layout = QVBoxLayout()
        for exercise_setting in self._topic_edited.exercise_settings:
            exercise_setting_widget = self._get_exercise_setting_widget(exercise_setting=exercise_setting)
            settings_layout.addWidget(exercise_setting_widget, alignment=Qt.AlignHCenter)

        layout.addLayout(settings_layout)

        icon = IconFactory.get_icon_widget(image_name='save.png')
        self._save_button = ButtonFactory.get_button_component(
            title='', function_to_connect=lambda: self._send_signal(save=True), icon=icon, icon_size=30,
            tooltip='Guardar', primary_button=True
        )
        layout.addWidget(self._save_button, alignment=Qt.AlignHCenter)

        self._save_label = LabelFactory.get_label_component(
            text=f'Guardado', label_type=TextType.NORMAL_TEXT, align=Qt.AlignHCenter, set_visible=False
        )
        self._save_label.setStyleSheet('color: green;')
        layout.addWidget(self._save_label, alignment=Qt.AlignHCenter)

        self._setup_exercise_checkbox_layout()
        self._setup_step_checkbox_layout()

        self.setLayout(layout)
        self.show()
        self.setFixedSize(self.width(), self.height())

    def _send_signal(self, save: bool = False):
        if save:
            for exercise_setting, exercise_setting_edited in zip(self._topic.exercise_settings,
                                                                 self._topic_edited.exercise_settings):
                exercise_setting.exercise_num = exercise_setting_edited.exercise_num
                exercise_setting.is_active = exercise_setting_edited.is_active

                for step_setting, step_setting_edited in zip(exercise_setting.step_settings,
                                                             exercise_setting_edited.step_settings):
                    step_setting.is_active = step_setting_edited.is_active

            self._topic = self._topic_edited
            TopicDataMapper.save_topic_configuration(self._topic_edited)
            self._save_label.setVisible(True)
        else:
            self.close_signal.emit()

    def _get_exercise_setting_widget(self, exercise_setting: ExerciseSetting) -> QWidget:
        widget = QWidget()
        widget.setObjectName('topic-container')
        widget.setStyleSheet("""
            #topic-container {
                border: 4px solid #897B6D;
                border-radius: 20px;
                background: #F5EBE0;
            }
        """)
        layout = QVBoxLayout()

        text_label = LabelFactory.get_label_component(
            text=f'{self._topic.title}', label_type=TextType.TITLE, align=Qt.AlignLeft,
            set_visible=True, set_bold=True
        )
        layout.addWidget(text_label, alignment=Qt.AlignLeft)

        slider_layout = QHBoxLayout()

        self._slider_label = LabelFactory.get_label_component(
            text=f'Número de ejercicios: {exercise_setting.exercise_num}', label_type=TextType.NORMAL_TEXT,
            align=Qt.AlignLeft, set_visible=True
        )
        slider_layout.addWidget(self._slider_label)
        slider = self._get_slider(exercise_setting=exercise_setting)
        slider_layout.addWidget(slider)
        layout.addLayout(slider_layout)

        checkbox = self._get_exercise_checkbox(exercise_setting=exercise_setting)
        self._checkbox_exercise_list.append(checkbox)
        layout.addWidget(checkbox)

        step_setting_layout = self._get_step_settings_layout(exercise_id=exercise_setting.id,
                                                             exercise_setting=exercise_setting)
        layout.addLayout(step_setting_layout)
        widget.setLayout(layout)
        return widget

    def _get_slider(self, exercise_setting: ExerciseSetting) -> QSlider:
        slider = QSlider(Qt.Horizontal)
        slider.setValue(exercise_setting.exercise_num)
        slider.setMinimum(1)
        max_num = 20 if exercise_setting.exercise_type == FunctionExerciseType.elementary_graph_exercise.value \
            else exercise_setting.max_exercise_num
        slider.setMaximum(max_num)
        slider.setTickInterval(1)
        slider.setTickPosition(QSlider.TicksBothSides)
        slider.setSingleStep(1)
        slider.valueChanged.connect(lambda value: self._on_slider_change(value, exercise_setting))
        return slider

    def _on_slider_change(self, value: int, exercise_setting: ExerciseSetting):
        exercise_setting.exercise_num = value
        self._slider_label.setText(f'Número de ejercicios: {value}')
        self._save_label.setVisible(False)

    def _get_exercise_checkbox(self, exercise_setting: ExerciseSetting) -> QCheckBox:
        checkbox = self._get_checkbox(initial_value=exercise_setting.is_active, text=exercise_setting.description)
        checkbox.clicked.connect(
            lambda value: self._set_exercise_checkbox(value=value, exercise_setting=exercise_setting)
        )
        return checkbox

    def _set_exercise_checkbox(self, value: int, exercise_setting: ExerciseSetting):
        exercise_setting.is_active = value
        if value:
            for checkbox in self._checkbox_exercise_list:
                checkbox.setDisabled(False)
        else:
            self._setup_exercise_checkbox_layout()

        self._save_label.setVisible(False)

    def _get_checkbox(self, initial_value: bool, text: str) -> QCheckBox:
        checkbox = QCheckBox()
        checkbox.setText(text)
        checkbox.setTristate(False)
        checkbox.setChecked(initial_value)
        return checkbox

    def _get_step_settings_layout(self, exercise_id: int, exercise_setting: ExerciseSetting) -> QVBoxLayout:
        layout = QVBoxLayout()

        text_label = LabelFactory.get_label_component(
            text=f'Selecciona los pasos a incluir en el ejercicio', label_type=TextType.NORMAL_TEXT, align=Qt.AlignLeft,
            set_visible=True, set_underline=True, set_bold=True
        )
        layout.addWidget(text_label, alignment=Qt.AlignLeft)

        for step_setting in exercise_setting.step_settings:
            checkbox = self._get_checkbox(initial_value=step_setting.is_active, text=step_setting.description)
            checkbox.clicked.connect(
                lambda value, step=step_setting: self._set_step_setting_active(value=value, step_setting=step,
                                                                               exercise_id=exercise_id)
            )
            layout.addWidget(checkbox)
            self._checkbox_step_list_by_exercise_id[exercise_id].append(checkbox)
        return layout

    def _set_step_setting_active(self, value: bool, exercise_id: int, step_setting: StepSetting):
        step_setting.is_active = value

        checkbox_list = self._checkbox_step_list_by_exercise_id[exercise_id]
        if value:
            for checkbox in checkbox_list:
                checkbox.setDisabled(False)
        else:
            checkbox_activated = [checkbox for checkbox in checkbox_list if checkbox.isChecked()]
            if len(checkbox_activated) == 1:
                checkbox_activated[0].setDisabled(True)

        self._save_label.setVisible(False)

    def _setup_exercise_checkbox_layout(self):
        checkbox_activated = [checkbox for checkbox in self._checkbox_exercise_list if checkbox.isChecked()]
        if len(checkbox_activated) == 1:
            checkbox_activated[0].setDisabled(True)

    def _setup_step_checkbox_layout(self):
        for checkbox_list in self._checkbox_step_list_by_exercise_id.values():
            checkbox_activated = [checkbox for checkbox in checkbox_list if checkbox.isChecked()]
            if len(checkbox_activated) == 1:
                checkbox_activated[0].setDisabled(True)

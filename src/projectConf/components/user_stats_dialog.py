from collections import defaultdict

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

from src.projectConf.data_mappers import TopicDataMapper
from src.projectConf.factories import LabelFactory
from src.projectConf.models.enums import TextType


class UserStatsDialog(QWidget):
    close_signal = pyqtSignal()

    def __init__(self):
        super(UserStatsDialog, self).__init__()
        self._step_type_by_exercise_type = {
            'InverseGraphExercise': [
                'ConceptInverseExercise', 'SelectionInverseExercise', 'DelimitedInverseExercise'
            ],
            'ConceptDomainExercise': [
                'IndicateDomainExercise', 'IndicateRangeExercise'
            ],
            'ElementaryGraphExercise': [
                'IndicateElementaryExercise', 'IndicateElementaryShiftExercise'
            ],
            'MaximumMinimumExercise': ['MaximumMinimumExercise'],
        }
        self._description_by_exercise_type = {
            'InverseGraphExercise': 'Funciones inversas',
            'ConceptDomainExercise': 'Dominio y recorrido',
            'ElementaryGraphExercise': 'Funciones elementales',
            'MaximumMinimumExercise': 'Máximos y mínimos',
        }
        self._description_by_step_type = {
            'ConceptInverseExercise': 'Indicar si existe inversa',
            'SelectionInverseExercise': 'Seleccionar la función inversa',
            'DelimitedInverseExercise': 'Restringir dominio para obtener inversa',
            'IndicateDomainExercise': 'Indicar el dominio del ejercicio',
            'IndicateRangeExercise': 'Indicar el rango del ejercicio',
            'IndicateElementaryExercise': 'Indicar la función elemental',
            'IndicateElementaryShiftExercise': 'Indicar el desplazamiento',
            'MaximumMinimumExercise': 'Indicar los máximos y mínimos',
        }

        self._resume_by_step = defaultdict(list)

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
        self.setWindowTitle('Estadísticas de usuario')

        layout = QVBoxLayout()

        self._resume_by_step = TopicDataMapper.get_resume_exercises()

        exercise_widgets = []
        for exercise_type, description in self._description_by_exercise_type.items():
            exercise_widgets.append(self._get_exercise_widget(exercise_type=exercise_type, description=description))

        for widget in exercise_widgets:
            layout.addWidget(widget)

        self.setLayout(layout)
        self.show()
        self.setFixedSize(self.width() + 100, self.height())

    def _get_exercise_widget(self, exercise_type: str, description: str) -> QWidget:
        label_text_layouts = []
        valid_total_num = 0
        total_total_num = 0
        for step_type in self._step_type_by_exercise_type[exercise_type]:
            valid_num, total_num = self._get_step_data(step_type=step_type)
            valid_total_num += valid_num
            total_total_num += total_num
            label_text = self._get_label_text_layout(description=self._description_by_step_type[step_type],
                                                     valid_num=valid_num, total_num=total_num)
            label_text_layouts.append(label_text)

        exercise_text_layout = self._get_label_text_layout(description=description, valid_num=valid_total_num,
                                                           total_num=total_total_num, is_exercise=True)

        widget = QWidget()
        widget.setObjectName('topic-container')
        widget.setStyleSheet("""
            #topic-container {
                border: 4px solid #897B6D;
                border-radius: 20px;
                background: #F5EBE0;
            }
        """)
        widget_layout = QVBoxLayout()
        widget_layout.addLayout(exercise_text_layout)
        widget_layout.addSpacing(10)
        for step_layout in label_text_layouts:
            widget_layout.addLayout(step_layout)
            widget_layout.addSpacing(2)

        widget.setLayout(widget_layout)
        return widget

    def _get_step_data(self, step_type: str):
        valid_num = 0
        total_num = len(self._resume_by_step[step_type])
        for resume in self._resume_by_step[step_type]:
            if resume.is_correct:
                valid_num += 1
        return valid_num, total_num

    def _get_label_text_layout(self, description: str, valid_num: int, total_num: int,
                               is_exercise: bool = False) -> QHBoxLayout:
        layout = QHBoxLayout()
        text_type = TextType.SUBTITLE if is_exercise else TextType.NORMAL_TEXT
        label_description = LabelFactory.get_label_component(
            text=description, label_type=text_type, set_visible=True
        )
        percentage = f'{valid_num // total_num * 100} %' if total_num else 'N/A'
        value = LabelFactory.get_label_component(
            text=percentage, label_type=text_type, set_visible=True
        )

        layout.addWidget(label_description)
        layout.addStretch()
        layout.addWidget(value)
        return layout

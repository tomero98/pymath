from typing import Union, List

import pyqtgraph
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal, QRegExp, Qt
from PyQt5.QtWidgets import QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QLabel
from pyqtgraph import LinearRegionItem

from src.projectConf.factories import ButtonFactory, LineEditFactory, LabelFactory, IconFactory
from src.projectConf.models.enums import TextType
from .graph_interaction_validation_component import GraphInteractionValidationComponent
from ...factories import PlotFactory2
from ...models import FunctionExercise, FunctionStep, ExerciseResume, Point


class DomainDefinitionComponent(GraphInteractionValidationComponent):
    continue_signal = pyqtSignal(bool)
    label = 'Indicar el dominio de la función'

    def __init__(self, exercise: FunctionExercise, step: FunctionStep, resume: ExerciseResume,
                 need_help_data: bool = False):
        super(DomainDefinitionComponent, self).__init__(
            exercise=exercise, step=step, resume=resume, need_help_data=need_help_data
        )

        self._proxy = None
        self._linear_region_items: List[LinearRegionItem] = []
        self._domain_expression_label: QLabel = None  # noqa
        self._domain_expression_edit_label: QLineEdit = None  # noqa
        self._create_range_button: QPushButton = None  # noqa

    def _setup_components(self):
        super(DomainDefinitionComponent, self)._setup_components()
        self._domain_expression_edit_layout = self._get_domain_expression_edit_layout()

    def _get_domain_expression_edit_layout(self) -> QHBoxLayout:
        layout = QHBoxLayout()

        self._domain_expression_label = LabelFactory.get_label_component(
            text='Dominio:', label_type=TextType.NORMAL_TEXT, align=Qt.AlignHCenter
        )
        self._domain_expression_edit_label = self._get_domain_expression_edit_label()
        layout.addStretch()
        layout.addWidget(self._domain_expression_label, alignment=Qt.AlignVCenter)
        layout.addWidget(self._domain_expression_edit_label)
        layout.addSpacing(15)
        layout.addWidget(self._validate_button, alignment=Qt.AlignTop)
        layout.addStretch()
        return layout

    def _get_domain_expression_edit_label(self) -> QLineEdit:
        domain_edit = LineEditFactory.get_line_edit_component(
            placeholder_text='(-inf, 3] U (5, +inf)', fixed_height=40, fixed_width=300,
            font_size=TextType.NORMAL_TEXT.value
        )
        regex = QRegExp('[\(\[0-9\-][\ ]*[\-+inf0-9]+[\ ]*,[\ ]*[\-+inf0-9]+[\ ]*[\)\]][\ ]*U[\ ]*' * 5)
        validator = QtGui.QRegExpValidator(regex)
        domain_edit.setValidator(validator)
        return domain_edit

    def _get_button_layout(self) -> QVBoxLayout:
        layout = super(DomainDefinitionComponent, self)._get_button_layout()

        self._create_range_button = self._get_create_range_button()
        layout.addStretch()
        layout.addWidget(self._create_range_button, alignment=Qt.AlignRight | Qt.AlignVCenter)
        layout.addStretch()
        return layout

    def _get_create_range_button(self) -> QPushButton:
        icon = IconFactory.get_icon_widget(image_name='plus.png')
        return ButtonFactory.get_button_component(
            title='', function_to_connect=self._on_click_create_range_button, secondary_button=True, icon=icon,
            icon_size=60, tooltip='Añadir rango', primary_button=True
        )

    def _on_click_create_range_button(self):
        linear_region_item = pyqtgraph.LinearRegionItem(values=(-1, 1), orientation='vertical', swapMode='sort',
                                                        bounds=(-1, 1))
        linear_region_item.sigRegionChangeFinished.connect(self._update_domain_expression_edit_label)
        self._linear_region_items.append(linear_region_item)
        self._plot_widget.addItem(linear_region_item)

    def _update_domain_expression_edit_label(self):
        pass

    def _setup_layout(self):
        self._layout.addWidget(self._question_label, alignment=Qt.AlignHCenter)
        self._layout.addSpacing(10)
        self._layout.addLayout(self._plot_widget_layout)
        self._layout.addSpacing(20)
        self._layout.addLayout(self._domain_expression_edit_layout)
        self._layout.addStretch()

    def _on_click_validation_button(self):
        self._validate_exercise(expression_selected=self._answers_by_point_type)

    def _get_correct_expression(self):
        return self._exercise._get_maximum_minimum_points()

    def _get_function_to_draw(self):
        return self._exercise.get_main_function()

    def _is_exercise_correct(self, expression_selected):
        correct_expression = self._get_correct_expression()
        return expression_selected == correct_expression

    def _validate_exercise(self, expression_selected: Union[dict, str], is_resume: bool = False):
        super()._validate_exercise(expression_selected=str(dict(expression_selected)), is_resume=is_resume)
        expression_selected = dict(expression_selected)
        correct_expression = self._get_correct_expression()

        for point_type, points in expression_selected:
            for point in points:
                if point not in correct_expression[point_type]:
                    self._set_point_on_validating(point=point, point_type=point_type, validation_type='wrong')

        for point_type, points in correct_expression:
            for point in points:
                if point not in expression_selected[point_type]:
                    self._set_point_on_validating(point=point, point_type=point_type, validation_type='missing')
                if point not in expression_selected[point_type]:
                    self._set_point_on_validating(point=point, point_type=point_type, validation_type='correct')

        self._post_exercise_validation(expression_selected=expression_selected)

    def _set_point_on_validating(self, point: Point, point_type: str, validation_type: str):
        point_color_text_by_validation_type = {
            'wrong': ('red', 'Incorrecto. '),
            'missing': ('orange', 'No seleccionado. '),
            'correct': ('green', 'Correcto. '),
        }
        color_point, text_point = point_color_text_by_validation_type[validation_type]

        PlotFactory2.set_points(graph=self._plot_widget, points=[point], color=color_point)

        point.y = point.y - 0.15
        PlotFactory2.set_labels2(
            graph=self._plot_widget, points=[(point, (color_point, f'{text_point}  {point_type}'))]
        )

    def _post_exercise_validation(self, expression_selected: dict):
        is_answer_correct = self._is_exercise_correct(expression_selected=expression_selected)
        if not is_answer_correct:
            self._help_text.setText('Incorrecto.')
            border_color = 'red'
        else:
            self._help_text.setText('Correcto.')
            border_color = '#2F8C53'

        self._help_text.setVisible(True)
        self._help_text.setStyleSheet(f'color: {border_color}')

        self._continue_button.setStyleSheet(f'background: {border_color}')
        self._continue_button.setDisabled(False)

        if self._exercise.exercise_order != 0 or self._step.order != 0:
            self._back_button.setDisabled(False)

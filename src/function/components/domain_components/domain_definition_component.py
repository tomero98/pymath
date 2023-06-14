from typing import Union, List

import pyqtgraph
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPen, QColor
from PyQt5.QtWidgets import QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QLabel
from pyqtgraph import LinearRegionItem

from src.projectConf.factories import ButtonFactory, LineEditFactory, LabelFactory, IconFactory
from src.projectConf.models.enums import TextType
from .graph_interaction_validation_component import GraphInteractionValidationComponent
from .range_selection_dialog import RangeSelectionDialog
from ...factories import PlotFactory2
from ...models import FunctionExercise, FunctionStep, ExerciseResume, Point


class DomainDefinitionComponent(GraphInteractionValidationComponent):
    continue_signal = pyqtSignal(bool)
    label = 'Indicar el dominio de la función'
    _ORIENTATION = 'vertical'
    _BORDER_COLOR_BY_BORDER_TYPE = {'inf': 'transparent', 'included': 'blue', 'not_included': 'red'}

    def __init__(self, exercise: FunctionExercise, step: FunctionStep, resume: ExerciseResume,
                 need_help_data: bool = False):
        super(DomainDefinitionComponent, self).__init__(
            exercise=exercise, step=step, resume=resume, need_help_data=need_help_data
        )

        self._proxy = None
        self._range_selection_dialog: RangeSelectionDialog = None  # noqa
        self._linear_region_items: List[LinearRegionItem] = []
        self._domain_expression_label: QLabel = None  # noqa
        self._domain_expression_edit_label: QLineEdit = None  # noqa
        self._create_range_button: QPushButton = None  # noqa
        self._delete_range_button: QPushButton = None  # noqa

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
            placeholder_text='', fixed_height=40, fixed_width=300, font_size=TextType.NORMAL_TEXT.value
        )
        domain_edit.setDisabled(True)
        return domain_edit

    def _get_button_layout(self) -> QVBoxLayout:
        layout = super(DomainDefinitionComponent, self)._get_button_layout()

        button_option_layout = self._get_button_option_layout()

        layout.addStretch()
        layout.addLayout(button_option_layout)
        layout.addStretch()
        return layout

    def _get_button_option_layout(self) -> QHBoxLayout:
        layout = QHBoxLayout()
        self._create_range_button = self._get_create_range_button()
        self._delete_range_button = self._get_delete_range_button()
        layout.addWidget(self._create_range_button, alignment=Qt.AlignRight | Qt.AlignVCenter)
        layout.addSpacing(20)
        layout.addWidget(self._delete_range_button, alignment=Qt.AlignRight | Qt.AlignVCenter)
        layout.addStretch()

        return layout

    def _get_create_range_button(self) -> QPushButton:
        icon = IconFactory.get_icon_widget(image_name='plus.png')
        return ButtonFactory.get_button_component(
            title='', function_to_connect=self._on_click_create_range_button, primary_button=True, icon=icon,
            icon_size=60, tooltip='Añadir rango'
        )

    def _on_click_create_range_button(self):
        if not self._range_selection_dialog:
            self._setup_range_selection_dialog()

    def _get_delete_range_button(self) -> QPushButton:
        icon = IconFactory.get_icon_widget(image_name='minus.png')
        return ButtonFactory.get_button_component(
            title='', function_to_connect=self._on_click_delete_range_button, primary_button=True, icon=icon,
            icon_size=60, tooltip='Eliminar el último rango añadido', is_disable=True
        )

    def _on_click_delete_range_button(self):
        if self._linear_region_items:
            linear_region_item = self._linear_region_items.pop()
            self._plot_widget.removeItem(linear_region_item)
            self._update_domain_expression_edit_label()

    def _setup_range_selection_dialog(self):
        self._range_selection_dialog = RangeSelectionDialog(
            plot_range=[self._exercise.plot_range[0], self._exercise.plot_range[1]], ranges_added=[]
        )
        self._range_selection_dialog.continue_signal.connect(self._add_range_selection_dialog)
        self._range_selection_dialog.draw()
        self._range_selection_dialog.delete_signal.connect(self._destroy_range_selection_dialog)

    def _add_range_selection_dialog(self, range_added: str):
        min_value = self._exercise.plot_range[0] - 0.1
        max_value = self._exercise.plot_range[1] + 0.1

        range_parts = range_added[1:-1].split(',')
        lower_limit = range_parts[0]
        upper_limit = range_parts[1]
        if lower_limit == '-inf':
            lower_bound = min_value
            lower_limit_type = 'inf'
        else:
            lower_bound = round(float(lower_limit), 2)
            lower_limit_type = 'included' if range_added[0] == '[' else 'not_included'

        if upper_limit == ' +inf':
            upper_bound = max_value
            upper_limit_type = 'inf'
        else:
            upper_bound = round(float(upper_limit), 2)
            upper_limit_type = 'included' if range_added[-1] == ']' else 'not_included'

        self._setup_new_linear_region_item(lower_bound=lower_bound, upper_bound=upper_bound, min_value=min_value,
                                           max_value=max_value, lower_limit_type=lower_limit_type,
                                           upper_limit_type=upper_limit_type)
        self._update_domain_expression_edit_label()

    def _setup_new_linear_region_item(self, lower_bound: float, upper_bound: float, min_value: float, max_value: float,
                                      lower_limit_type: str, upper_limit_type: str):
        linear_region_item = pyqtgraph.LinearRegionItem(values=(lower_bound, upper_bound), orientation='vertical',
                                                        swapMode='sort', bounds=(min_value, max_value))

        linear_region_item.sigRegionChangeFinished.connect(self._update_domain_expression_edit_label)
        first_border_color = QPen(QColor(self._BORDER_COLOR_BY_BORDER_TYPE[lower_limit_type]))
        first_border_color.setWidth(0.2)
        linear_region_item.lines[0].setPen(first_border_color)
        second_border_color = QPen(QColor(self._BORDER_COLOR_BY_BORDER_TYPE[upper_limit_type]))
        second_border_color.setWidth(0.2)
        linear_region_item.lines[1].setPen(second_border_color)

        self._linear_region_items.append(linear_region_item)
        self._plot_widget.addItem(linear_region_item)
        self._range_selection_dialog = None

    def _update_domain_expression_edit_label(self):
        limits = []
        for region_item in self._linear_region_items:
            bounds = region_item.getRegion()
            lower_limit = '('
            lower_value = round(float(bounds[0]), 2)
            upper_limit = ')'
            upper_value = round(float(bounds[1]), 2)
            domain = f'{lower_limit}{lower_value}, {upper_value}{upper_limit}'
            limits.append(domain)

        text = ' U '.join(limits)
        self._domain_expression_edit_label.setText(text)

        if not self._linear_region_items:
            self._delete_range_button.setDisabled(True)
        else:
            self._delete_range_button.setDisabled(False)

    def _destroy_range_selection_dialog(self):
        self._range_selection_dialog = None

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

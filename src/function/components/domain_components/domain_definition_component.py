from typing import List

import pyqtgraph
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPen, QColor
from PyQt5.QtWidgets import QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QWidget
from pyqtgraph import LinearRegionItem

from src.projectConf.factories import ButtonFactory, LineEditFactory, LabelFactory, IconFactory
from src.projectConf.models.enums import TextType
from .graph_interaction_validation_component import GraphInteractionValidationComponent
from .range_selection_dialog import RangeSelectionDialog
from ...factories import PlotFactory2
from ...models import FunctionExercise, FunctionStep, ExerciseResume, Function
from ...models.enums import ResumeState


class DomainDefinitionComponent(GraphInteractionValidationComponent):
    continue_signal = pyqtSignal(bool)

    label = 'Indicar el dominio de la función'
    _ORIENTATION = 'vertical'
    _BORDER_COLOR_BY_BORDER_TYPE = {'inf': 'transparent', 'included': 'blue', 'not_included': 'red'}

    def __init__(self, exercise: FunctionExercise, step: FunctionStep, resume: ExerciseResume,
                 need_help_data: bool = False, show_main_function_limits: bool = True,
                 show_function_labels: bool = False):
        super(DomainDefinitionComponent, self).__init__(
            exercise=exercise, step=step, resume=resume, need_help_data=need_help_data,
            show_main_function_limits=show_main_function_limits, show_function_labels=show_function_labels
        )

        self._proxy = None
        self._selected_linear_range_item: LinearRegionItem = None  # noqa
        self._range_selection_dialog: RangeSelectionDialog = None  # noqa
        self._linear_region_items: List[LinearRegionItem] = []
        self._domain_expression_label: QLabel = None  # noqa
        self._domain_expression_edit_label: QLineEdit = None  # noqa
        self._create_range_button: QPushButton = None  # noqa
        self._delete_range_button: QPushButton = None  # noqa
        self._result_label: QLabel = None  # noqa
        self._validate_button: QPushButton = None  # noqa

    def _setup_components(self):
        super(DomainDefinitionComponent, self)._setup_components()
        self._validate_button = self._get_validate_button()
        self._validate_button.setDisabled(True)
        self._domain_expression_edit_widget = self._get_domain_expression_edit_widget()

    def _get_domain_expression_edit_widget(self) -> QWidget:
        widget = QWidget()
        widget.setObjectName('topic-container')

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

        widget.setLayout(layout)
        return widget

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

    def _get_plot_widget(self) -> pyqtgraph.PlotWidget:
        plot = super(DomainDefinitionComponent, self)._get_plot_widget()
        self._proxy = pyqtgraph.SignalProxy(plot.scene().sigMouseClicked, rateLimit=60, slot=self._plot_clicked)
        return plot

    def _plot_clicked(self, event):
        if self._resume.resume_state != ResumeState.pending:
            return None

        pos = event[0].scenePos()
        if not self._range_selection_dialog and self._plot_widget.sceneBoundingRect().contains(pos):
            pos = self._plot_widget.getPlotItem().vb.mapSceneToView(pos)
            linear_ranges_clicked = [
                linear_range for linear_range in self._linear_region_items if linear_range.contains(pos)
            ]
            if linear_ranges_clicked:
                linear_ranges_clicked_order = sorted(
                    linear_ranges_clicked, key=lambda x: abs(x.getRegion()[1] - x.getRegion()[0])
                )
                domain_expression = self._get_domain_expression_from_linear_region_item(linear_ranges_clicked_order[0])
                self._setup_range_selection_dialog(domain_expression=domain_expression)
                self._selected_linear_range_item = linear_ranges_clicked_order[0]
                self._create_range_button.setDisabled(True)

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
            self._create_range_button.setDisabled(True)

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

    def _setup_range_selection_dialog(self, domain_expression: str = ''):
        self._range_selection_dialog = RangeSelectionDialog(
            plot_range=[self._exercise.plot_range[0], self._exercise.plot_range[1]], ranges_added=[],
            range_item=domain_expression
        )
        self._range_selection_dialog.continue_signal.connect(self._add_range_selection_dialog)
        self._range_selection_dialog.draw()
        self._range_selection_dialog.delete_signal.connect(self._destroy_range_selection_dialog)

    def _add_range_selection_dialog(self, range_added: str):
        min_value = self._exercise.plot_range[0]
        max_value = self._exercise.plot_range[1]

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
                                           upper_limit_type=upper_limit_type,
                                           linear_region_item=self._selected_linear_range_item)
        self._update_domain_expression_edit_label()
        self._create_range_button.setDisabled(False)
        self._selected_linear_range_item = None

    def _setup_new_linear_region_item(self, lower_bound: float, upper_bound: float, min_value: float, max_value: float,
                                      lower_limit_type: str, upper_limit_type: str,
                                      linear_region_item: LinearRegionItem = None):
        if not linear_region_item:
            linear_region_item = pyqtgraph.LinearRegionItem(values=(lower_bound, upper_bound), orientation='vertical',
                                                            swapMode='block', bounds=(min_value, max_value))
            linear_region_item.sigRegionChangeFinished.connect(self._update_domain_expression_edit_label)
            self._linear_region_items.append(linear_region_item)
            self._plot_widget.addItem(linear_region_item)
        else:
            linear_region_item.setRegion([lower_bound, upper_bound])

        hover_color = QPen(QColor('green'))
        hover_color.setWidth(0.2)

        first_border_color = QPen(QColor(self._BORDER_COLOR_BY_BORDER_TYPE[lower_limit_type]))
        first_border_color.setWidth(0.2)
        linear_region_item.lines[0].setPen(first_border_color)
        linear_region_item.lines[0].setHoverPen(hover_color)
        second_border_color = QPen(QColor(self._BORDER_COLOR_BY_BORDER_TYPE[upper_limit_type]))
        second_border_color.setWidth(0.2)
        linear_region_item.lines[1].setPen(second_border_color)
        linear_region_item.lines[1].setHoverPen(hover_color)

        if self._range_selection_dialog:
            self._range_selection_dialog.close()
            self._range_selection_dialog = None

    def _update_domain_expression_edit_label(self):
        limits = []
        for region_item in self._linear_region_items:
            expression = self._get_domain_expression_from_linear_region_item(region_item)
            limits.append(expression)

        text = ' U '.join(limits)
        self._domain_expression_edit_label.setText(text)

        if not self._linear_region_items:
            self._delete_range_button.setDisabled(True)
            self._validate_button.setDisabled(True)
        else:
            self._delete_range_button.setDisabled(False)
            self._validate_button.setDisabled(False)

    def _get_domain_expression_from_linear_region_item(self, region_item: LinearRegionItem) -> str:
        bounds = region_item.getRegion()

        lower_bound_color = region_item.lines[0].pen.color()
        lower_value = round(float(bounds[0]), 2)

        if not lower_bound_color.red() and not lower_bound_color.blue() and lower_value != self._exercise.plot_range[0]:
            not_included_bound_color = QPen(QColor(self._BORDER_COLOR_BY_BORDER_TYPE['not_included']))
            not_included_bound_color.setWidth(0.2)
            region_item.lines[0].setPen(not_included_bound_color)
            lower_bound_color = region_item.lines[0].pen.color()

        if lower_bound_color.red():
            lower_limit = '('
        elif lower_bound_color.blue():
            lower_limit = '['
        else:
            lower_limit = '('
            lower_value = '-inf'

        upper_bound_color = region_item.lines[1].pen.color()
        upper_value = round(float(bounds[1]), 2)

        if not upper_bound_color.red() and not upper_bound_color.blue() and upper_value != self._exercise.plot_range[1]:
            not_included_bound_color = QPen(QColor(self._BORDER_COLOR_BY_BORDER_TYPE['not_included']))
            not_included_bound_color.setWidth(0.2)
            region_item.lines[1].setPen(not_included_bound_color)
            upper_bound_color = region_item.lines[1].pen.color()

        if upper_bound_color.red():
            upper_limit = ')'
        elif upper_bound_color.blue():
            upper_limit = ']'
        else:
            upper_limit = ')'
            upper_value = '+inf'

        return f'{lower_limit}{lower_value}, {upper_value}{upper_limit}'

    def _destroy_range_selection_dialog(self):
        self._range_selection_dialog.close()
        self._range_selection_dialog = None
        self._create_range_button.setDisabled(False)
        self._selected_linear_range_item = None

    def _setup_layout(self):
        self._layout.addWidget(self._question_label, alignment=Qt.AlignHCenter)
        self._layout.addSpacing(10)
        self._layout.addWidget(self._plot_widget_container, alignment=Qt.AlignTop | Qt.AlignHCenter)
        self._layout.addSpacing(20)
        self._layout.addWidget(self._domain_expression_edit_widget, alignment=Qt.AlignHCenter)
        self._layout.addWidget(self._result_label, alignment=Qt.AlignHCenter)
        self._layout.addStretch()

    def _on_click_validation_button(self):
        self._validate_exercise(expression_selected=self._domain_expression_edit_label.text())

    def _get_function_to_draw(self) -> Function:
        return self._exercise.get_main_function()

    def _validate_exercise(self, expression_selected: str, is_resume: bool = False):
        super()._validate_exercise(expression_selected=expression_selected, is_resume=is_resume)

        if is_resume:
            self._setup_user_range(range_expression=expression_selected)

        for region_item in self._linear_region_items:
            region_item.setMovable(False)

        is_correct, user_wrong_domain_num_set, user_missed_domain_num_set = \
            self._exercise.validate_domain_expression(user_domain_input=expression_selected)
        if is_correct:
            self._setup_correct_response()
        else:
            self._setup_wrong_response(
                correct_response=self._exercise.get_domain_expression(),
                user_wrong_domain_num_set=user_wrong_domain_num_set,
                user_missed_domain_num_set=user_missed_domain_num_set
            )
        self._setup_finished_exercise()

    def _setup_user_range(self, range_expression: str):
        range_expression_list = range_expression.split(' U ')
        for expression in range_expression_list:
            self._add_range_selection_dialog(range_added=expression)

    def _setup_correct_response(self):
        self._result_label.setText('Correcto.')
        self._result_label.setStyleSheet('color: green')
        self._result_label.setVisible(True)

    def _setup_wrong_response(self, correct_response: str, user_wrong_domain_num_set: set,
                              user_missed_domain_num_set: set):
        self._result_label.setText(f'Incorrecto. El dominio de la función es el siguiente: {correct_response}')
        self._result_label.setStyleSheet('color: red')
        self._result_label.setVisible(True)

        if user_wrong_domain_num_set:
            slice_num = max(len(user_wrong_domain_num_set) // 3, 1)
            sorted_wrong_num_set = sorted(user_wrong_domain_num_set)
            x_points = set(sorted_wrong_num_set[::slice_num])
            self._setup_constant_points(x_points=x_points, color='red')

        if user_missed_domain_num_set:
            slice_num = max(len(user_missed_domain_num_set) // 3, 1)
            sorted_missed_num_set = sorted(user_missed_domain_num_set)
            x_points = set(sorted_missed_num_set[::slice_num])
            self._setup_constant_points(x_points=x_points, color='red')

    def _setup_constant_points(self, x_points: set, color: str):
        if self._ORIENTATION == 'vertical':
            points_list = [
                ([x_point, x_point], [self._exercise.plot_range[0], self._exercise.plot_range[1]])
                for x_point in x_points
            ]
        else:
            points_list = [
                ([self._exercise.plot_range[0], self._exercise.plot_range[1]], [x_point, x_point])
                for x_point in x_points
            ]
        for point_list in points_list:
            PlotFactory2.set_graph_using_points(
                graph=self._plot_widget, x_values=point_list[0], y_values=point_list[1], color=color, function_width=1.5
            )

    def _is_exercise_correct(self, expression_selected: str) -> bool:
        is_correct, _, _ = self._exercise.validate_domain_expression(user_domain_input=expression_selected)
        return is_correct

    def _on_function_to_draw_click(self, plot_curve_item_selected, point_selected):
        return None

    def _setup_finished_exercise(self):
        super(DomainDefinitionComponent, self)._setup_finished_exercise()
        self._validate_button.setDisabled(True)
        if self._create_range_button:
            self._create_range_button.setDisabled(True)
        if self._delete_range_button:
            self._delete_range_button.setDisabled(True)

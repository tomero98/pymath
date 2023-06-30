from collections import defaultdict
from typing import Union

import pyqtgraph
from PyQt5.QtCore import pyqtSignal, Qt, QSize, QPointF
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel

from src.projectConf.factories import LabelFactory
from src.projectConf.models.enums import TextType
from .point_selection_dialog import PointSelectionDialog
from ..inverse_components import InverseSelectionComponent
from ...factories import PlotFactory2
from ...models import FunctionExercise, FunctionStep, ExerciseResume, Point


class MaximumMinimumComponent(InverseSelectionComponent):
    continue_signal = pyqtSignal(bool)
    label = 'Seleccionar máximos y mínimos'

    def __init__(self, exercise: FunctionExercise, step: FunctionStep, resume: ExerciseResume,
                 need_help_data: bool = False):
        super(MaximumMinimumComponent, self).__init__(
            exercise=exercise, step=step, resume=resume, need_help_data=need_help_data, show_main_function_limits=True
        )
        self._point_info_by_point_type = {
            'máximo absoluto': (255, 0, 0), 'máximo relativo': (200, 0, 0), 'mínimo absoluto': (0, 0, 255),
            'mínimo relativo': (0, 0, 200),
        }

        self._point_selection_dialog: PointSelectionDialog = None  # noqa
        self._answers_by_point_type: defaultdict = defaultdict(list)
        self._proxy = None
        self._proxy2 = None
        self._coordinates_label: QLabel = None  # noqa
        self._resolved: bool = False

    def _setup_data(self):
        main_functions = self._exercise.get_main_function()
        for main_function in main_functions:
            main_function.setup_domain_data(self._exercise.plot_range)

    def _setup_layout(self):
        self._layout.addWidget(self._question_label, alignment=Qt.AlignHCenter)
        self._layout.addSpacing(10)
        self._layout.addWidget(self._plot_widget_container, alignment=Qt.AlignTop | Qt.AlignHCenter)
        self._layout.addWidget(self._coordinates_label, alignment=Qt.AlignHCenter)
        self._layout.addSpacing(20)
        self._layout.addWidget(self._validate_button, alignment=Qt.AlignHCenter)
        self._layout.addWidget(self._result_label, alignment=Qt.AlignHCenter)
        self._layout.addStretch()

    def _on_click_validation_button(self):
        self._validate_exercise(expression_selected=self._answers_by_point_type)
        self._validate_button.setDisabled(True)

    def _get_correct_expression(self):
        return self._exercise.get_maximum_minimum_points()

    def _get_function_to_draw(self):
        return self._exercise.get_main_function()

    def _is_exercise_correct(self, expression_selected):
        correct_expression = self._get_correct_expression()
        clean_correct_expression = {key: value for key, value in correct_expression.items() if value is not None}
        clean_expression_selected = {key: value for key, value in eval(expression_selected).items() if
                                     value is not None}
        return clean_expression_selected == clean_correct_expression

    def _on_function_to_draw_click(self, plot_curve_item_selected, point_selected):
        if not isinstance(point_selected, tuple):
            point = point_selected.pos()
            point_to_draw = Point(x=point.x(), y=point.y())
        else:
            point_to_draw = Point(x=point_selected[0], y=point_selected[1])
        point_to_draw.truncate(decimals=2)

        if not self._point_selection_dialog:
            self._setup_point_selection_dialog(point_to_draw=point_to_draw)

    def _get_plot_widget(self) -> pyqtgraph.PlotWidget:
        plot_widget = PlotFactory2.get_plot(function_range=self._exercise.plot_range)
        PlotFactory2.set_functions(
            graph=plot_widget, functions=self._exercise.get_main_function(), function_width=5, color='white',
            show_limits=self._show_main_function_limits, click_function=self._on_function_to_draw_click
        )
        self._proxy = pyqtgraph.SignalProxy(plot_widget.scene().sigMouseMoved, rateLimit=60, slot=self.mouse_moved)
        self._proxy2 = pyqtgraph.SignalProxy(plot_widget.scene().sigMouseClicked, rateLimit=60, slot=self.mouse_click)
        self._set_point_graphs(plot_widget=plot_widget)
        return plot_widget

    def _set_point_graphs(self, plot_widget: pyqtgraph.PlotWidget):
        for point in self._exercise.exercise_points:
            color = 'w' if point.is_included else 'black'
            PlotFactory2.set_points(graph=plot_widget, points=[point], color=color,
                                    click_function=self._on_function_to_draw_click)

    def _setup_components(self):
        super(MaximumMinimumComponent, self)._setup_components()
        self._validate_button = self._get_validate_button()
        self._coordinates_label = LabelFactory.get_label_component(
            text='', label_type=TextType.SUBTITLE, align=Qt.AlignHCenter, need_word_wrap=True, set_visible=False
        )

    def _get_validate_button(self) -> QWidget:
        validate_button = super(MaximumMinimumComponent, self)._get_validate_button()
        widget = QWidget()
        widget.setObjectName('topic-container')

        layout = QHBoxLayout()
        layout.addWidget(validate_button, alignment=Qt.AlignTop | Qt.AlignHCenter)

        widget.setLayout(layout)
        widget.setMinimumSize(QSize(widget.minimumSizeHint().width() * 1.4, widget.minimumSizeHint().height() * 1.2))
        return widget

    def mouse_moved(self, e):
        pos = e[0]
        if self._plot_widget.sceneBoundingRect().contains(pos) and not self._resolved:
            mouse_point = self._plot_widget.getPlotItem().vb.mapSceneToView(pos)
            x_position = float('%.2f' % (mouse_point.x()))
            y_position = float('%.2f' % (mouse_point.y()))
            self._coordinates_label.setText(f'Punto ({x_position}, {y_position})')
            self._coordinates_label.setVisible(True)

    def mouse_click(self, e):
        pos = e[0].scenePos()
        if self._plot_widget.sceneBoundingRect().contains(pos) and not self._resolved:
            mouse_point = self._plot_widget.getPlotItem().vb.mapSceneToView(pos)
            x_position = float('%.2f' % (mouse_point.x()))
            y_position = float('%.2f' % (mouse_point.y()))
            self._coordinates_label.setText(f'Punto ({x_position}, {y_position})')
            self._coordinates_label.setVisible(True)
            self._on_function_to_draw_click(plot_curve_item_selected=None, point_selected=(x_position, y_position))

    def _setup_point_selection_dialog(self, point_to_draw: Point):
        self._point_selection_dialog = PointSelectionDialog(point=point_to_draw)
        self._point_selection_dialog.continue_signal.connect(self._set_point_to_graph)
        self._point_selection_dialog.close_signal.connect(self._close_dialog)
        self._point_selection_dialog.draw()

    def _set_point_to_graph(self, point_type: str, point_to_draw: Point, y_constant: str, x_range_for_y: str):
        color_point = self._point_info_by_point_type[point_type]

        if point_to_draw.x is not None and point_to_draw.y is not None:
            PlotFactory2.set_points(graph=self._plot_widget, points=[point_to_draw], color=color_point)
            self._answers_by_point_type[point_type].append(point_to_draw.serialize())

            text_point = str(point_to_draw)
            point_to_draw.y = point_to_draw.y - 0.15
            PlotFactory2.set_labels2(graph=self._plot_widget, points=[(point_to_draw, (color_point, text_point))])

            point_to_draw.y = point_to_draw.y - 0.2
            PlotFactory2.set_labels2(graph=self._plot_widget, points=[(point_to_draw, (color_point, point_type))])
        self._update_with_constant_points(y_constant=y_constant, x_range_for_y=x_range_for_y, point_type=point_type,
                                          color=color_point)
        self._point_selection_dialog.close()
        self._point_selection_dialog = None

    def _update_with_constant_points(self, y_constant: str, x_range_for_y: str, point_type: str, color: str):
        if y_constant == '' or x_range_for_y == '':
            return None

        y_constant = round(float(y_constant), 2)
        x_range_for_y_split = x_range_for_y[1: -1].split(',')
        first_x = round(float(x_range_for_y_split[0]), 2)
        last_x = round(float(x_range_for_y_split[-1]), 2)
        nums = []
        x_value = first_x
        x_points = []
        y_points = []
        while x_value <= last_x:
            if first_x == x_value and x_range_for_y[0] == '(':
                x_value += 0.01
                continue

            if x_value == last_x and x_range_for_y[-1] == ')':
                x_value += 0.01
                continue

            x_points.append(x_value)
            y_points.append(y_constant)
            nums.append((x_value, y_constant))
            x_value += 0.01
            x_value = round(x_value, 2)

        if x_points:
            self._answers_by_point_type[point_type].extend(nums)
            PlotFactory2.set_graph_using_points(
                graph=self._plot_widget, x_values=x_points, y_values=y_points, function_width=5, color=color
            )
            positive_shift = ['máximo absoluto', 'máximo relativo']
            label_shift = 0.7 if point_type in positive_shift else - 0.7

            point_to_draw = Point(x_points[len(x_points) // 2], y_points[len(x_points) // 2] + label_shift)
            point_to_draw.y = point_to_draw.y - 0.15
            PlotFactory2.set_labels2(graph=self._plot_widget, points=[(point_to_draw, (color, f'{x_range_for_y}'))])

            point_to_draw.y = point_to_draw.y - 0.2
            PlotFactory2.set_labels2(graph=self._plot_widget, points=[(point_to_draw, (color, point_type))])

    def _close_dialog(self):
        self._point_selection_dialog = None

    def _validate_exercise(self, expression_selected: Union[dict, str], is_resume: bool = False):
        super(InverseSelectionComponent, self)._validate_exercise(expression_selected=str(dict(expression_selected)),
                                                                  is_resume=is_resume)
        expression_selected = dict(expression_selected)
        correct_expression = self._get_correct_expression()
        self._resolved = True
        self._coordinates_label.setVisible(False)
        # is_answer_correct = self._is_exercise_correct(expression_selected=str(dict(expression_selected)))
        # if not is_answer_correct:
        #     PlotFactory2.reset_graph(self._plot_widget)
        #     PlotFactory2.set_functions(
        #         graph=self._plot_widget, functions=self._exercise.get_main_function(), function_width=5, color='white',
        #         show_limits=self._show_main_function_limits, click_function=self._on_function_to_draw_click
        #     )
        wrong_points_by_y_point_type = defaultdict(list)
        missing_points_by_y_point_type = defaultdict(list)
        for point_type, points in expression_selected.items():
            if points is None:
                continue

            for point in points:
                if point not in correct_expression[point_type]:
                    key = (point[1], point_type)
                    wrong_points_by_y_point_type[key].append(point[0])

        for point_type, points in correct_expression.items():
            if points is None:
                continue

            for point in points:
                if point not in expression_selected.get(point_type, []):
                    key = (point[1], point_type)
                    missing_points_by_y_point_type[key].append(point[0])

        self._setup_wrong(wrong_points_by_y_point_type=wrong_points_by_y_point_type,
                          missing_points_by_y_point_type=missing_points_by_y_point_type)

        if self._is_exercise_correct(expression_selected=str(dict(expression_selected))):
            self._setup_correct_response()
        else:
            self._setup_wrong_response()

    def _set_point_on_validating(self, point: Point, point_type: str, validation_type: str):
        point_color_text_by_validation_type = {
            'wrong': ('red', 'Incorrecto. '),
            'missing': ('orange', 'No seleccionado. '),
            'correct': ('green', 'Correcto. '),
        }
        color_point, text_point = point_color_text_by_validation_type[validation_type]

        PlotFactory2.set_points(graph=self._plot_widget, points=[point], color=color_point)

        point_to_draw = point
        text_point = str(point_to_draw)
        point_to_draw.y = point_to_draw.y - 0.15
        PlotFactory2.set_labels2(graph=self._plot_widget, points=[(point_to_draw, (color_point, text_point))])

        point_to_draw.y = point_to_draw.y - 0.2
        PlotFactory2.set_labels2(graph=self._plot_widget, points=[(point_to_draw, (color_point, point_type))])

    def _setup_correct_response(self, *args, **kwargs):
        self._result_label.setText('Correcto.')
        self._result_label.setStyleSheet('color: green;')
        self._result_label.setVisible(True)

    def _setup_wrong_response(self, *args, **kwargs):
        self._result_label.setText('Incorrecto.')
        self._result_label.setStyleSheet('color: red;')
        self._result_label.setVisible(True)

    def _setup_wrong(self, wrong_points_by_y_point_type: dict, missing_points_by_y_point_type: dict):
        for key, wrong_points in wrong_points_by_y_point_type.items():
            y_value, point_type = key
            if len(wrong_points) > 1:
                split_y_points = []
                y_points_grouped = []
                previous_point = None
                for point in sorted(wrong_points):
                    if previous_point is None:
                        previous_point = point
                        y_points_grouped.append(point)
                        continue

                    if abs(point - previous_point) > 0.2:
                        split_y_points.append(y_points_grouped)
                        y_points_grouped = []

                    y_points_grouped.append(point)
                    previous_point = point

                if y_points_grouped:
                    split_y_points.append(y_points_grouped)

                for x_group in split_y_points:
                    y_points = [y_value] * len(x_group)
                    PlotFactory2.set_graph_using_points(
                        graph=self._plot_widget, x_values=x_group, y_values=y_points, function_width=5,
                        color='red'
                    )

            elif len(wrong_points) == 1:
                point = Point(x=wrong_points[0], y=y_value)
                self._set_point_on_validating(point=point, point_type=point_type, validation_type='missing')

        for key, missing_points in missing_points_by_y_point_type.items():
            y_value, point_type = key
            if len(missing_points) > 1:
                split_y_points = []
                y_points_grouped = []
                previous_point = None
                for point in sorted(missing_points):
                    if previous_point is None:
                        previous_point = point
                        y_points_grouped.append(point)
                        continue

                    if abs(point - previous_point) > 0.2:
                        split_y_points.append(y_points_grouped)
                        y_points_grouped = []

                    y_points_grouped.append(point)
                    previous_point = point

                if y_points_grouped:
                    split_y_points.append(y_points_grouped)

                for x_group in split_y_points:
                    y_points = [y_value] * len(x_group)
                    PlotFactory2.set_graph_using_points(
                        graph=self._plot_widget, x_values=x_group, y_values=y_points, function_width=5,
                        color='orange'
                    )

                    positive_shift = ['máximo absoluto', 'máximo relativo']
                    label_shift = 0.7 if point_type in positive_shift else -0.2

                    point_to_draw = Point(x_group[len(x_group) // 2], y_value + label_shift)
                    point_to_draw.y = point_to_draw.y - 0.15
                    PlotFactory2.set_labels2(
                        graph=self._plot_widget,
                        points=[(point_to_draw, ('orange', f'[{x_group[0]}, {x_group[-1]}]'))])

                    point_to_draw.y = point_to_draw.y - 0.2
                    PlotFactory2.set_labels2(graph=self._plot_widget, points=[(point_to_draw, ('orange', point_type))])

            elif len(missing_points) == 1:
                point = Point(x=missing_points[0], y=y_value)
                self._set_point_on_validating(point=point, point_type=point_type, validation_type='missing')

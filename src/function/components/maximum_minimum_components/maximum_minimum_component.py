from collections import defaultdict
from typing import Union

import pyqtgraph
from PyQt5.QtCore import pyqtSignal

from .point_selection_dialog import PointSelectionDialog
from ..graph_interaction_validation_component import GraphInteractionValidationComponent
from ...factories import PlotFactory2
from ...models import FunctionExercise, FunctionStep, ExerciseResume, Point


class MaximumMinimumComponent(GraphInteractionValidationComponent):
    continue_signal = pyqtSignal(bool)
    label = 'Seleccionar máximos y mínimos'

    def __init__(self, exercise: FunctionExercise, step: FunctionStep, resume: ExerciseResume,
                 need_help_data: bool = False):
        super(MaximumMinimumComponent, self).__init__(
            exercise=exercise, step=step, resume=resume, need_help_data=need_help_data, need_validate_button=True,
            add_interaction_to_main_graph=True
        )
        self._point_info_by_point_type = {
            'máximo absoluto': (255, 0, 0), 'máximo relativo': (200, 0, 0), 'mínimo absoluto': (0, 0, 255),
            'mínimo relativo': (0, 0, 200),
        }

        self._point_selection_dialog: PointSelectionDialog = None  # noqa
        self._answers_by_point_type: defaultdict = defaultdict(list)
        self._proxy = None

    def _on_click_validation_button(self):
        self._validate_exercise(expression_selected=self._answers_by_point_type)

    def _get_correct_expression(self):
        return self._exercise._get_maximum_minimum_points()

    def _get_function_to_draw(self):
        return self._exercise.get_main_function()

    def _is_exercise_correct(self, expression_selected):
        correct_expression = self._get_correct_expression()
        return expression_selected == correct_expression

    def _on_function_to_draw_click(self, plot_curve_item_selected, point_selected):
        point = point_selected.pos()
        point_to_draw = Point(x=point.x(), y=point.y())
        point_to_draw.truncate(decimals=1)

        if not self._point_selection_dialog:
            self._setup_point_selection_dialog(point_to_draw=point_to_draw)

    def _set_plot_widget(self):
        super(MaximumMinimumComponent, self)._set_plot_widget()
        self._proxy = pyqtgraph.SignalProxy(self._plot_widget.scene().sigMouseMoved, rateLimit=60, slot=self.mouse_moved)

    def mouse_moved(self, e):
        pos = e[0]
        if self._plot_widget.sceneBoundingRect().contains(pos):
            mouse_point = self._plot_widget.getPlotItem().vb.mapSceneToView(pos)
            x_position = round(mouse_point.x(), 1)
            y_position = round(mouse_point.y(), 1)
            self._coordinates_label.setText(f'Punto ({x_position}, {y_position})')
            self._coordinates_label.setVisible(True)

    def _setup_point_selection_dialog(self, point_to_draw: Point):
        self._point_selection_dialog = PointSelectionDialog(point=point_to_draw)
        self._point_selection_dialog.continue_signal.connect(self._set_point_to_graph)
        self._point_selection_dialog.draw()

    def _set_point_to_graph(self, point_type: str, point_to_draw: Point):
        color_point = self._point_info_by_point_type[point_type]

        PlotFactory2.set_points(graph=self._plot_widget, points=[point_to_draw], color=color_point)

        text_point = str(point_to_draw)
        point_to_draw.y = point_to_draw.y - 0.15
        PlotFactory2.set_labels2(graph=self._plot_widget, points=[(point_to_draw, (color_point, text_point))])

        point_to_draw.y = point_to_draw.y - 0.2
        PlotFactory2.set_labels2(graph=self._plot_widget, points=[(point_to_draw, (color_point, point_type))])

        self._answers_by_point_type[point_type].append(point_to_draw)
        self._point_selection_dialog.close()
        self._point_selection_dialog = None

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

from typing import Tuple

import pyqtgraph
from PyQt5.QtCore import pyqtSignal

from ..graph_interaction_component import GraphInteractionComponent
from ...models import FunctionExercise, FunctionStep, ExerciseResume, Function


class InverseDelimitedComponent(GraphInteractionComponent):
    continue_signal = pyqtSignal(bool)
    label = 'Seleccionar la inversa'

    def __init__(self, exercise: FunctionExercise, step: FunctionStep, resume: ExerciseResume,
                 need_help_data: bool = False):
        super(InverseDelimitedComponent, self).__init__(
            exercise=exercise, step=step, resume=resume, need_help_data=need_help_data, need_validate_button=True
        )

        self._region: pyqtgraph.LinearRegionItem = None  # noqa

    def _get_correct_expression(self, *args, **kwargs):
        return 'no-duplicates'

    def _get_function_to_draw(self):
        return self._exercise.get_main_function()

    def _is_exercise_correct(self, expression_selected):
        main_function = self._exercise.get_main_function()
        y_values_selected = [y for x, y in zip(main_function.x_values, main_function.y_values)
                             if expression_selected[0] <= x <= expression_selected[1]]
        return len(set(y_values_selected)) == len(y_values_selected)

    def _set_plot_widget(self):
        super(InverseDelimitedComponent, self)._set_plot_widget()
        self._region = pyqtgraph.LinearRegionItem(values=(-1, 1), orientation='vertical', swapMode='sort')
        self._plot_widget.addItem(self._region)

    def _on_click_validation_button(self):
        response = self._region.getRegion()
        expression_selected = f'{response[0]}, {response[1]}'
        self._validate_exercise(expression_selected=expression_selected)

    def _validate_exercise(self, expression_selected: str, is_resume: bool = False):
        expression_selected = tuple(map(float, expression_selected.split(',')))
        super()._validate_exercise(expression_selected=expression_selected, is_resume=is_resume)
        is_answer_correct = self._is_exercise_correct(expression_selected=expression_selected)
        self._set_exercise(expression_selected=expression_selected, is_answer_correct=is_answer_correct)

    def _set_exercise(self, expression_selected: Tuple, is_answer_correct: bool):
        border_color = '#2F8C53' if is_answer_correct else 'red'
        if not is_answer_correct:
            self._help_text.setText('Incorrecto.')
            self._update_region_with_error(expression_selected=expression_selected)
        else:
            self._region.setMovable(False)
            self._help_text.setText('Correcto.')
        self._help_text.setVisible(True)
        self._help_text.setStyleSheet(f'color: {border_color}')

        self._continue_button.setStyleSheet(f'background: {border_color}')
        self._continue_button.setDisabled(False)

        if self._exercise.exercise_order != 0 or self._step.order != 0:
            self._back_button.setDisabled(False)

    def _update_region_with_error(self, expression_selected: Tuple[float, float]):
        self._region.setRegion((expression_selected[0], expression_selected[1]))
        self._region.setMovable(False)
        self._region.setBrush((255, 0, 0))
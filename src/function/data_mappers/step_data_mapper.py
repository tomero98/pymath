from typing import List

from .help_data_mapper import HelpDataMapper
from ..models import FunctionExercise, FunctionStep
from ..models.enums import FunctionExerciseType, StepType


class StepDataMapper:
    def __init__(self, exercise: FunctionExercise):
        self._exercise: FunctionExercise = exercise
        self._help_data_mapper = HelpDataMapper(exercise=exercise)

    def get_steps(self) -> List[FunctionStep]:
        steps = []
        if self._exercise.type == FunctionExerciseType.inverse_graph_exercise.value:
            steps = self._get_inverse_graph_exercise_steps()
        elif self._exercise.type == FunctionExerciseType.domain_concept_exercise.value:
            steps = self._get_domain_concept_exercise_steps()
        elif self._exercise.type == FunctionExerciseType.elementary_graph_exercise.value:
            steps = self._get_elementary_graph_exercise_steps()
        elif self._exercise.type == FunctionExerciseType.maximum_points_exercise.value:
            steps = self._get_maximum_points_exercise_steps()
        return steps

    def _get_inverse_graph_exercise_steps(self) -> List[FunctionStep]:
        first_step = self._get_first_inverse_concept_step()
        second_step = self._get_second_inverse_concept_step(exercise=self._exercise)
        # return [first_step, second_step]
        return [second_step]

    def _get_first_inverse_concept_step(self) -> FunctionStep:
        step_type = StepType.inverse_concept_exercise
        question = 'Indica si la siguiente gráfica tiene inversa para todo el dominio mostrado'
        order = 0
        help_data_list = self._help_data_mapper.get_help_data(step_type=step_type)
        return FunctionStep(step_type=step_type, question=question, order=order, help_data_list=help_data_list)

    def _get_second_inverse_concept_step(self, exercise: FunctionExercise) -> FunctionStep:
        function_has_inverse = exercise.has_main_function_inverse()
        return self._get_inverse_select_step() if function_has_inverse else self._get_delimited_inverse_range_step()

    def _get_inverse_select_step(self):
        step_type = StepType.selection_inverse_exercise
        question = 'Selecciona la gráfica que representa la inversa en el dominio dado para la función:'
        order = 1
        help_data_list = self._help_data_mapper.get_help_data(step_type=step_type)
        return FunctionStep(step_type=step_type, question=question, order=order, help_data_list=help_data_list)

    @staticmethod
    def _get_delimited_inverse_range_step():
        step_type = StepType.delimited_inverse_exercise
        question = 'Delimita el rango de la función para que tenga inversa'
        order = 1
        return FunctionStep(step_type=step_type, question=question, order=order)

    def _get_domain_concept_exercise_steps(self) -> List[FunctionStep]:
        first_step = self._get_first_domain_concept_step()
        second_step = self._get_second_domain_concept_step()
        return [first_step, second_step]

    def _get_first_domain_concept_step(self) -> FunctionStep:
        step_type = StepType.indicate_domain_exercise
        question = 'Con la ayuda del ratón, indica el dominio de la función representada.'
        order = 0
        help_data_list = self._help_data_mapper.get_help_data(step_type=step_type)
        return FunctionStep(step_type=step_type, question=question, order=order, help_data_list=help_data_list)

    def _get_second_domain_concept_step(self) -> FunctionStep:
        step_type = StepType.indicate_range_exercise
        question = 'Con la ayuda del ratón, indica el recorrido de la función representada.'
        order = 1
        help_data_list = self._help_data_mapper.get_help_data(step_type=step_type)
        return FunctionStep(step_type=step_type, question=question, order=order, help_data_list=help_data_list)

    def _get_elementary_graph_exercise_steps(self):
        first_step = self._get_first_elementary_graph_step()
        second_step = self._get_second_elementary_graph_step()
        # return [first_step, second_step]
        return [second_step]

    @staticmethod
    def _get_first_elementary_graph_step():
        step_type = StepType.indicate_elementary_exercise
        question = 'Selecciona la expresión de la gráfica mostrada:'
        order = 0
        return FunctionStep(step_type=step_type, question=question, order=order, help_data_list=None)

    def _get_second_elementary_graph_step(self):
        step_type = StepType.indicate_elementary_shift_exercise
        question = 'Selecciona la expresión de la gráfica mostrada:'
        order = 1
        help_data_list = self._help_data_mapper.get_help_data(step_type)
        return FunctionStep(step_type=step_type, question=question, order=order, help_data_list=help_data_list)

    def _get_maximum_points_exercise_steps(self):
        first_step = self._get_first_maximum_point_step()
        second_step = self._get_second_maximum_point_step()
        return [first_step, second_step]

    def _get_first_maximum_point_step(self):
        step_type = StepType.maximum_relative_exercise
        question = 'Con ayuda del ratón, encuentra los máximos relativos de la función representada:'
        order = 1
        help_data = self._help_data_mapper.get_help_data(step_type=step_type)
        return FunctionStep(step_type=step_type, question=question, order=order, help_data=help_data)

    def _get_second_maximum_point_step(self):
        step_type = StepType.maximum_absolute_exercise
        question = 'Con ayuda del ratón, encuentra los máximos absolutos de la función representada:'
        order = 1
        help_data = self._help_data_mapper.get_help_data(step_type=step_type)
        return FunctionStep(step_type=step_type, question=question, order=order, help_data=help_data)

    def _get_minimum_points_exercise_steps(self):
        first_step = self._get_first_minimum_point_step()
        second_step = self._get_second_minimum_point_step()
        return [first_step, second_step]

    def _get_first_minimum_point_step(self):
        step_type = StepType.minimum_relative_exercise
        question = 'Con ayuda del ratón, encuentra los mínimos relativos de la función representada:'
        order = 1
        help_data = self._help_data_mapper.get_help_data(step_type=step_type)
        return FunctionStep(step_type=step_type, question=question, order=order, help_data=help_data)

    def _get_second_minimum_point_step(self):
        step_type = StepType.minimum_absolute_exercise
        question = 'Con ayuda del ratón, encuentra los mínimos absolutos de la función representada:'
        order = 1
        help_data = self._help_data_mapper.get_help_data(step_type=step_type)
        return FunctionStep(step_type=step_type, question=question, order=order, help_data=help_data)

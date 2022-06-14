from typing import List

from .help_data_mapper import HelpDataMapper
from ..models.enums.inverse_exercise_type import FunctionExerciseType
from ..models.enums.inverse_step_type import InverseStepType
from ..models.function_exercise import FunctionExercise
from ..models.function_step import FunctionStep


class StepDataMapper:
    def __init__(self, exercise: FunctionExercise):
        self._help_data_mapper = HelpDataMapper()
        self._exercise = exercise

    def get_steps(self) -> List[FunctionStep]:
        steps = []
        if self._exercise.type == FunctionExerciseType.inverse_concept_exercise.value:
            steps = self._get_inverse_concept_exercise_steps(exercise=self._exercise)
        elif self._exercise.type == FunctionExerciseType.domain_concept_exercise.value:
            steps = self._get_domain_concept_exercise_steps(exercise=self._exercise)
        return steps

    def _get_inverse_concept_exercise_steps(self, exercise: FunctionExercise) -> List[FunctionStep]:
        first_step = self._get_first_inverse_concept_step()
        second_step = self._get_second_inverse_concept_step(exercise=exercise)
        return [first_step, second_step]

    def _get_first_inverse_concept_step(self) -> FunctionStep:
        identifier = 0
        step_type = InverseStepType.boolean_inverse_exercise
        question = '¿La siguiente gráfica tiene inversa?'
        order = 0
        function_help_data = self._help_data_mapper.get_help_data(exercise=self._exercise, step_type=step_type)
        return FunctionStep(identifier=identifier, step_type=step_type, question=question, order=order,
                            function_help_data=function_help_data)

    def _get_second_inverse_concept_step(self, exercise: FunctionExercise) -> FunctionStep:
        function_has_inverse = exercise.has_main_function_inverse()
        step = self._get_inverse_select_step() if function_has_inverse else self._get_delimited_inverse_range_step()
        return step

    def _get_inverse_select_step(self):
        identifier = 0
        step_type = InverseStepType.selection_inverse_exercise
        question = 'Selecciona la gráfica que representa la inversa en el dominio dado para la función:'
        order = 1
        function_help_data = self._help_data_mapper.get_help_data(exercise=self._exercise, step_type=step_type)
        return FunctionStep(identifier=identifier, step_type=step_type, question=question, order=order,
                            function_help_data=function_help_data)

    @staticmethod
    def _get_delimited_inverse_range_step():
        identifier = 0
        step_type = InverseStepType.delimited_inverse_exercise
        question = 'Delimita el rango de la función para que tenga inversa'
        order = 1
        return FunctionStep(identifier=identifier, step_type=step_type, question=question, order=order)

    def _get_domain_concept_exercise_steps(self, exercise: FunctionExercise) -> List[FunctionStep]:
        first_step = self._get_first_domain_concept_step()
        return [first_step]

    def _get_first_domain_concept_step(self) -> FunctionStep:
        identifier = 0
        step_type = InverseStepType.indicate_domain_exercise
        question = 'Indica el dominio y el recorrido de la siguiente gráfica'
        order = 0
        function_help_data = self._help_data_mapper.get_help_data(exercise=self._exercise, step_type=step_type)
        return FunctionStep(identifier=identifier, step_type=step_type, question=question, order=order,
                            function_help_data=function_help_data)

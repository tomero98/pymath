from .help_data_mapper import HelpDataMapper
from .step_info_data_mapper import StepInfoDataMapper
from ..models import FunctionExercise, FunctionStep
from ..models.enums import StepType
from ...projectConf.models import ExerciseSetting


class StepDataMapper:
    def __init__(self, exercise: FunctionExercise, exercise_setting: ExerciseSetting):
        self._exercise: FunctionExercise = exercise
        self._exercise_setting: ExerciseSetting = exercise_setting
        self._help_data_mapper = HelpDataMapper(exercise=exercise)
        self._step_info_data_mapper = StepInfoDataMapper()

    def get_steps(self):
        for step_setting in self._exercise_setting.step_settings:
            if not step_setting.is_active:
                continue

            step = None
            if step_setting.step_type == StepType.inverse_concept_exercise.value:
                step = self._get_inverse_concept_exercise_step()
            elif step_setting.step_type == StepType.selection_inverse_exercise.value \
                    and self._exercise.has_main_function_inverse():
                step = self._get_selection_inverse_exercise_step()
            elif step_setting.step_type == StepType.delimited_inverse_exercise.value \
                    and not self._exercise.has_main_function_inverse():
                step = self._get_delimited_inverse_exercise_step()

            elif step_setting.step_type == StepType.indicate_domain_exercise.value:
                step = self._get_indicate_domain_exercise_step()
            elif step_setting.step_type == StepType.indicate_range_exercise.value:
                step = self._get_indicate_range_exercise_step()

            elif step_setting.step_type == StepType.indicate_elementary_exercise.value:
                step = self._get_indicate_elementary_exercise_step()
            elif step_setting.step_type == StepType.indicate_elementary_shift_exercise.value:
                step = self._get_indicate_elementary_shift_exercise_step()

            elif step_setting.step_type == StepType.maximum_minimum_exercise.value:
                step = self._get_maximum_minimum_exercise_step()

            if step:
                self._exercise.steps.append(step)

    def _get_inverse_concept_exercise_step(self) -> FunctionStep:
        step_type = StepType.inverse_concept_exercise
        question = 'Indica si la siguiente función tiene inversa para todo el dominio mostrado.'
        order = 0
        help_data_list = self._help_data_mapper.get_help_data(step_type=step_type)
        step_info_data = self._step_info_data_mapper.get_step_info_data(step_type=step_type)
        return FunctionStep(step_type=step_type, question=question, order=order, help_data_list=help_data_list,
                            step_info_data=step_info_data)

    def _get_selection_inverse_exercise_step(self):
        step_type = StepType.selection_inverse_exercise
        question = 'Selecciona la función inversa de la función blanca.'
        order = 1
        help_data_list = self._help_data_mapper.get_help_data(step_type=step_type)
        step_info_data = self._step_info_data_mapper.get_step_info_data(step_type=step_type)
        return FunctionStep(step_type=step_type, question=question, order=order, help_data_list=help_data_list,
                            step_info_data=step_info_data)

    def _get_delimited_inverse_exercise_step(self):
        step_type = StepType.delimited_inverse_exercise
        question = 'Delimita el rango de la función para que tenga inversa.'
        order = 2
        help_data_list = self._help_data_mapper.get_help_data(step_type=step_type)
        step_info_data = self._step_info_data_mapper.get_step_info_data(step_type=step_type)
        return FunctionStep(step_type=step_type, question=question, order=order, step_info_data=step_info_data,
                            help_data_list=help_data_list)

    def _get_indicate_domain_exercise_step(self) -> FunctionStep:
        step_type = StepType.indicate_domain_exercise
        question = 'Crea intervalos utilizando el botón de añadir para indicar el dominio de la función representada.'
        order = 0
        help_data_list = self._help_data_mapper.get_help_data(step_type=step_type)
        step_info_data = self._step_info_data_mapper.get_step_info_data(step_type=step_type)
        return FunctionStep(step_type=step_type, question=question, order=order, help_data_list=help_data_list,
                            step_info_data=step_info_data)

    def _get_indicate_range_exercise_step(self) -> FunctionStep:
        step_type = StepType.indicate_range_exercise
        question = 'Crea intervalos utilizando el botón de añadir para indicar el recorrido de la función representada.'
        order = 1
        help_data_list = self._help_data_mapper.get_help_data(step_type=step_type)
        step_info_data = self._step_info_data_mapper.get_step_info_data(step_type=step_type)
        return FunctionStep(step_type=step_type, question=question, order=order, help_data_list=help_data_list,
                            step_info_data=step_info_data)

    def _get_indicate_elementary_exercise_step(self):
        step_type = StepType.indicate_elementary_exercise
        question = 'Selecciona la expresión de la función representada.'
        order = 0
        step_info_data = self._step_info_data_mapper.get_step_info_data(step_type=step_type)
        return FunctionStep(step_type=step_type, question=question, order=order, help_data_list=None,
                            step_info_data=step_info_data)

    def _get_indicate_elementary_shift_exercise_step(self):
        step_type = StepType.indicate_elementary_shift_exercise
        question = 'Selecciona la expresión de la función representada.'
        order = 1
        help_data_list = self._help_data_mapper.get_help_data(step_type)
        step_info_data = self._step_info_data_mapper.get_step_info_data(step_type=step_type)
        return FunctionStep(step_type=step_type, question=question, order=order, help_data_list=help_data_list,
                            step_info_data=step_info_data)

    def _get_maximum_minimum_exercise_step(self):
        step_type = StepType.maximum_minimum_exercise
        question = 'Con ayuda del ratón, encuentra los máximos y mínimos relativos y absolutos:'
        order = 0
        help_data_list = self._help_data_mapper.get_help_data(step_type=step_type)
        step_info_data = self._step_info_data_mapper.get_step_info_data(step_type=step_type)
        return FunctionStep(step_type=step_type, question=question, order=order, help_data_list=help_data_list,
                            step_info_data=step_info_data)

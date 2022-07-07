from typing import List

from PyQt5.QtSql import QSqlQuery

from .step_data_mapper import StepDataMapper
from ..models.function import Function
from ..models.function_exercise import FunctionExercise


class FunctionExerciseDataMapper:
    @classmethod
    def get_function_exercise(cls, topic_id: int) -> List[FunctionExercise]:
        query = cls._get_function_exercise_query(topic_id=topic_id)
        result = QSqlQuery()
        result.exec(query)

        exercises_by_id = {}
        while result.next():
            exercise_id = result.value('exercise_id')
            if exercise_id not in exercises_by_id:
                exercise_type = result.value('exercise_type')
                title = FunctionExercise.get_title_by_exercise_type(exercise_type=exercise_type)
                exercise_order = result.value('exercise_order')
                domain = result.value('exercise_domain')
                domain = (-5, 5) if not bool(domain) else tuple(map(int, domain.split(',')))
                exercise = FunctionExercise(
                    identifier=exercise_id, exercise_type=exercise_type, exercise_order=exercise_order,
                    exercise_domain=domain, title=title, functions=[], steps=[]
                )
                exercises_by_id[exercise_id] = exercise

            exercise = exercises_by_id[exercise_id]
            function_id = result.value('graph_id')
            function_expression = result.value('graph_expression')
            function_domain = result.value('graph_domain')
            function_domain = function_domain if bool(function_domain) \
                else f'({exercise.exercise_domain[0] - 1}, {exercise.exercise_domain[1] + 1})'
            is_main_graphic = bool(result.value('is_main_graphic'))
            is_elementary_graph = bool(result.value('is_elementary_graph'))
            inverse_function = None
            inverse_function_id = bool(result.value('inverse_id'))
            if inverse_function_id:
                inverse_expression = result.value('inverse_expression')
                inverse_domain = result.value('inverse_domain')
                inverse_domain = inverse_domain if bool(inverse_domain) \
                    else f'({exercise.exercise_domain[0] - 1}, {exercise.exercise_domain[1] + 1})'
                inverse_function = Function(function_id=inverse_function_id, expression=inverse_expression,
                                            domain=inverse_domain, is_main_graphic=False,
                                            is_elementary_graph=False, inverse_function=None)
            function = Function(function_id=function_id, expression=function_expression, domain=function_domain,
                                is_main_graphic=is_main_graphic, inverse_function=inverse_function,
                                is_elementary_graph=is_elementary_graph)
            exercise.functions.append(function)

        for exercise in exercises_by_id.values():
            step_mapper = StepDataMapper(exercise=exercise)
            steps = step_mapper.get_steps()
            exercise.steps = steps
        return list(exercises_by_id.values())

    @staticmethod
    def _get_function_exercise_query(topic_id: int):
        return f'''
            SELECT exercises.id                    AS exercise_id,
                   exercises.type                  AS exercise_type,
                   exercises."order"               AS exercise_order,
                   exercises.domain                AS exercise_domain,
                   graphs.id                       AS graph_id,
                   graphs.expression               AS graph_expression,
                   exercise_graphs.is_main_graphic AS is_main_graphic,
                   exercise_graphs.domain          AS graph_domain,
                   graphs.is_elementary_graph      AS is_elementary_graph,
                   inverse_graphs.id               AS inverse_id,
                   inverse_graphs.expression       AS inverse_expression,
                   inverse_exercise_graph.domain   AS inverse_domain
            FROM exercises
                     INNER JOIN exercise_graphs ON exercises.id = exercise_graphs.exercise_id
                     INNER JOIN graphs ON exercise_graphs.graph_id = graphs.id
                     LEFT JOIN graphs inverse_graphs ON graphs.id = inverse_graphs.inverse_graph_id
                     LEFT JOIN exercise_graphs inverse_exercise_graph ON 
                            inverse_exercise_graph.exercise_id = exercises.id 
                        AND
                            inverse_exercise_graph.graph_id = inverse_graphs.inverse_graph_id
            WHERE exercises.topic_id == {topic_id} 
        '''

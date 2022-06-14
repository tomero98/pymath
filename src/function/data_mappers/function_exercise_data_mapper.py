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
                title = result.value('exercise_title')
                exercise_order = result.value('exercise_order')
                exercise_priority = result.value('exercise_priority')
                exercise = FunctionExercise(
                    identifier=exercise_id, exercise_type=exercise_type, exercise_order=exercise_order,
                    exercise_priority=exercise_priority, title=title, functions=[], steps=[]
                )
                exercises_by_id[exercise_id] = exercise

            exercise = exercises_by_id[exercise_id]
            function_id = result.value('graph_id')
            function_expression = result.value('graph_expression')
            function_domain = result.value('graph_domain')
            is_main_graphic = bool(result.value('is_main_graphic'))
            inverse_function = None
            inverse_function_id = bool(result.value('inverse_id'))
            if inverse_function_id:
                inverse_expression = result.value('inverse_expression')
                inverse_domain = result.value('inverse_domain')
                inverse_function = Function(function_id=inverse_function_id, expression=inverse_expression,
                                            domain=inverse_domain, is_main_graphic=False, inverse_function=None)
            function = Function(function_id=function_id, expression=function_expression, domain=function_domain,
                                is_main_graphic=is_main_graphic, inverse_function=inverse_function)
            exercise.functions.append(function)

        for exercise in exercises_by_id.values():
            step_mapper = StepDataMapper(exercise=exercise)
            steps = step_mapper.get_steps()
            exercise.steps = steps
        return list(exercises_by_id.values())

    @staticmethod
    def _get_function_exercise_query(topic_id: int):
        return f'''
            SELECT exercises.id as exercise_id, exercises.type as exercise_type, exercises.title as exercise_title,
            exercises.help_text as help_text, exercises."order" as exercise_order,
            exercises.priority as exercise_priority, graphs.id as graph_id, graphs.expression as graph_expression,
            graphs.domain as graph_domain, exercise_graphs.is_main_graphic as is_main_graphic,
            inverse_graphs.id as inverse_id, inverse_graphs.expression as inverse_expression,
            inverse_graphs.domain as inverse_domain
            FROM exercises
            INNER JOIN exercise_graphs ON exercises.id = exercise_graphs.exercise_id
            INNER JOIN graphs ON exercise_graphs.graph_id = graphs.id
            LEFT JOIN graphs inverse_graphs ON graphs.id = inverse_graphs.inverse_graph_id
            where exercises.topic_id == {topic_id} 
        '''

import itertools
import random
from typing import List

from copy import deepcopy
from PyQt5.QtSql import QSqlQuery

from .step_data_mapper import StepDataMapper
from ..models import Function, FunctionExercise, Point
from ..models.enums import FunctionExerciseType
from ...projectConf.models import Topic


class FunctionExerciseDataMapper:
    @classmethod
    def get_function_exercise(cls, topic: Topic) -> List[FunctionExercise]:
        # TODO CODE IMPROVE: mover a una clase el acceso a bd
        exercise_ids = cls._get_exercise_ids(topic=topic)
        query = cls._get_function_exercise_query(exercise_ids=exercise_ids)
        result = QSqlQuery()
        result.exec(query)

        exercises_by_id = {}
        exercise_order = 0
        while result.next():
            exercise_id = result.value('exercise_id')
            if exercise_id not in exercises_by_id:
                exercise = cls._initialize_exercise_values(query_result=result, exercise_order=exercise_order)
                exercises_by_id[exercise_id] = exercise
                exercise_order += 1
            exercise = exercises_by_id[exercise_id]
            cls._setup_exercises(query_result=result, exercise=exercise)

        exercises = list(exercises_by_id.values())
        if exercises[0].type == FunctionExerciseType.elementary_graph_exercise.value:
            exercises = cls._setup_elementary_graph(main_exercise=exercises[0], topic=topic)

        if exercises[0].type == FunctionExerciseType.maximum_minimum_exercise.value:
            cls._setup_maximum_graph(exercises=exercises)

        cls._setup_steps(exercises=exercises, topic=topic)
        return [exercise for exercise in exercises if exercise.steps]

    @classmethod
    def _get_exercise_ids(cls, topic: Topic) -> List[int]:
        exercise_ids = []
        where_clause = f'WHERE topic_id = {topic.id}'

        for exercise_setting in topic.exercise_settings:
            result = QSqlQuery()

            if exercise_setting.is_active:
                where_clause = f"{where_clause} AND exercise_type = '{exercise_setting.exercise_type}'"
                query = f"""
                    SELECT id
                    FROM exercises
                    {where_clause}
                    ORDER BY RANDOM()
                    LIMIT {exercise_setting.exercise_num}
                """
                result.exec(query)

                while result.next():
                    exercise_ids.append(result.value('id'))

        return exercise_ids

    @staticmethod
    def _get_function_exercise_query(exercise_ids: List[int]):
        return f'''
            SELECT exercises.id                    AS exercise_id,
                   exercises.exercise_type         AS exercise_type,
                   exercises.domain                AS exercise_domain,
                   graphs.id                       AS graph_id,
                   graphs.expression               AS graph_expression,
                   exercise_graphs.is_main_graphic AS is_main_graphic,
                   exercise_graphs.domain          AS graph_domain
            FROM exercises
            INNER JOIN exercise_graphs ON exercises.id = exercise_graphs.exercise_id
            INNER JOIN graphs ON exercise_graphs.graph_id = graphs.id
            WHERE exercises.id IN ({', '.join(list(map(str, exercise_ids)))})
            ORDER BY RANDOM()
        '''

    @staticmethod
    def _initialize_exercise_values(query_result: QSqlQuery, exercise_order: int) -> FunctionExercise:
        exercise_id = query_result.value('exercise_id')
        exercise_type = query_result.value('exercise_type')
        title = FunctionExercise.get_title_by_exercise_type(exercise_type=exercise_type)
        domain = query_result.value('exercise_domain')
        domain = (-5, 5) if not bool(domain) else tuple(map(int, domain.split(',')))
        return FunctionExercise(identifier=exercise_id, exercise_type=exercise_type, plot_range=domain,
                                title=title, functions=[], steps=[], exercise_order=exercise_order, exercise_points=[])

    @staticmethod
    def _setup_exercises(query_result: QSqlQuery, exercise: FunctionExercise) -> None:
        function_id = query_result.value('graph_id')
        function_expression = query_result.value('graph_expression')

        function_domain = query_result.value('graph_domain')
        domain = function_domain if bool(function_domain) else '(-inf, +inf)'
        if function_domain:
            domain_parts = function_domain[1:-1].replace(' ', '').split(',')
            first_part = exercise.plot_range[0] - 1 if domain_parts[0] == '-inf' else int(domain_parts[0])
            last_part = exercise.plot_range[-1] + 1 if domain_parts[-1] == '+inf' else int(domain_parts[-1])
            x_values_range = (first_part, last_part)
        else:
            x_values_range = (exercise.plot_range[0] - 1, exercise.plot_range[1] + 1)

        is_main_graphic = bool(query_result.value('is_main_graphic'))
        function = Function(function_id=function_id, expression=function_expression, x_values_range=x_values_range,
                            is_main_graphic=is_main_graphic, domain=domain)
        exercise.functions.append(function)

    @staticmethod
    def _setup_elementary_graph(main_exercise: FunctionExercise, topic: Topic) -> List[FunctionExercise]:
        setting = next(
            setting for setting in topic.exercise_settings
            if setting.exercise_type == FunctionExerciseType.elementary_graph_exercise.value
        )

        num_function_per_exercise = 4

        function_combination_group = list(
            itertools.combinations([function for function in main_exercise.functions], num_function_per_exercise)
        )

        exercises = []
        for i in range(setting.exercise_num):
            index_function_combination_group = random.randint(0, len(function_combination_group) - 1)
            functions = function_combination_group[index_function_combination_group]
            exercise = FunctionExercise(identifier=i, exercise_type=main_exercise.type, title=main_exercise.title,
                                        plot_range=main_exercise.plot_range, functions=deepcopy(functions),
                                        steps=[], exercise_order=i)
            exercises.append(exercise)
            index = random.randint(0, num_function_per_exercise - 1)
            exercise.functions[index].is_main_graphic = True
        return exercises

    @staticmethod
    def _setup_maximum_graph(exercises: List[FunctionExercise]):
        exercise_by_exercise_id = {exercise.id: exercise for exercise in exercises}
        exercise_ids = list(exercise_by_exercise_id.keys())
        result = QSqlQuery()
        query = f"""
                    SELECT *
                    FROM exercise_graph_points
                    WHERE exercise_id IN ({', '.join(list(map(str, exercise_ids)))})
            """
        result.exec(query)

        while result.next():
            exercise_id = result.value('exercise_id')
            x_value = result.value('x_value')
            y_value = result.value('y_value')
            is_included = bool(result.value('is_included'))
            point = Point(x=x_value, y=y_value, is_included=is_included)
            exercise_by_exercise_id[exercise_id].exercise_points.append(point)


    @staticmethod
    def _setup_steps(exercises: List[FunctionExercise], topic: Topic) -> None:
        exercise_setting_by_exercise_type = {
            setting.exercise_type: setting for setting in topic.exercise_settings
        }
        for exercise in exercises:
            setting = exercise_setting_by_exercise_type[exercise.type]
            step_mapper = StepDataMapper(exercise=exercise, exercise_setting=setting)
            step_mapper.get_steps()

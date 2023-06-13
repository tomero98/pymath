import random
from typing import List

from PyQt5.QtSql import QSqlQuery

from .step_data_mapper import StepDataMapper
from ..models import Function, FunctionExercise
from ..models.enums import FunctionExerciseType


class FunctionExerciseDataMapper:
    @classmethod
    def get_function_exercise(cls, topic_id: int) -> List[FunctionExercise]:
        # TODO CODE IMPROVE: mover a una clase el acceso a bd
        query = cls._get_function_exercise_query(topic_id=topic_id)
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
            exercises = cls._setup_elementary_graph(main_exercise=exercises[0])

        cls._setup_steps(exercises=exercises)
        return exercises

    @staticmethod
    def _get_function_exercise_query(topic_id: int):
        # TODO CUSTOM NUM EXERCISES
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
            WHERE exercises.topic_id == {topic_id}
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
                                title=title, functions=[], steps=[], exercise_order=exercise_order)

    @staticmethod
    def _setup_exercises(query_result: QSqlQuery, exercise: FunctionExercise) -> None:
        function_id = query_result.value('graph_id')
        function_expression = query_result.value('graph_expression')

        function_domain = query_result.value('graph_domain')
        domain = function_domain if bool(function_domain) else '(-inf, +inf)'
        x_values_range = tuple(map(int, function_domain[1:-1].split(','))) if bool(function_domain) \
            else (exercise.plot_range[0] - 1, exercise.plot_range[1] + 1)

        is_main_graphic = bool(query_result.value('is_main_graphic'))
        function = Function(function_id=function_id, expression=function_expression, x_values_range=x_values_range,
                            is_main_graphic=is_main_graphic, domain=domain)
        function.setup_data(plot_range=exercise.plot_range)
        exercise.functions.append(function)

    @staticmethod
    def _setup_elementary_graph(main_exercise: FunctionExercise) -> List[FunctionExercise]:
        # TODO CUSTOM NUM EXERCISES
        import itertools
        list_functions = list(itertools.combinations([function for function in main_exercise.functions], 4))
        exercises = []
        for i in range(4):
            index = random.randint(0, len(list_functions))
            functions = list_functions[index]
            exercise = FunctionExercise(identifier=i, exercise_type=main_exercise.type, title=main_exercise.title,
                                        plot_range=main_exercise.plot_range, functions=[*functions],
                                        steps=main_exercise.steps, exercise_order=i)
            exercises.append(exercise)
            index = random.randint(0, 3)
            exercise.functions[index].is_main_graphic = True
        return exercises

    @staticmethod
    def _setup_steps(exercises: List[FunctionExercise]) -> None:
        for exercise in exercises:
            step_mapper = StepDataMapper(exercise=exercise)
            steps = step_mapper.get_steps()
            exercise.steps = steps

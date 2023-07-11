from collections import defaultdict

from PyQt5.QtSql import QSqlQuery

from ..database import DatabaseAccessSingleton
from ..models import Topic, StepSetting, ExerciseSetting
from ..models.resume import Resume


class TopicDataMapper:
    @classmethod
    def get_topics(cls):
        max_num_exercise_by_exercise_type = cls._get_max_num_exercise_by_exercise_type()
        result = DatabaseAccessSingleton.get_topics_result()

        topic_by_id = {}
        exercise_setting_by_id = {}

        topics = []
        while result.next():
            identifier = result.value('topic_id')
            if identifier not in topic_by_id:
                topic = cls._get_topic_from_query(result=result)
                topic_by_id[topic.id] = topic
                topics.append(topic)
            topic = topic_by_id[identifier]

            exercise_setting_id = result.value('exercise_setting_id')
            if exercise_setting_id not in exercise_setting_by_id:
                exercise_setting = cls._get_exercise_setting_from_query(
                    result=result, max_num_exercise_by_exercise_type=max_num_exercise_by_exercise_type
                )
                exercise_setting_by_id[exercise_setting.id] = exercise_setting
                topic.exercise_settings.append(exercise_setting)
            exercise_setting = exercise_setting_by_id[exercise_setting_id]

            step_setting = cls._get_step_setting_from_query(result=result)
            exercise_setting.step_settings.append(step_setting)

        return topics

    @classmethod
    def _get_max_num_exercise_by_exercise_type(cls) -> dict:
        result = DatabaseAccessSingleton.get_max_nums_exercise_result()

        max_num_exercise_by_exercise_type = {}
        while result.next():
            exercise_type = result.value('exercise_type')
            exercise_count = result.value('exercise_count')
            max_num_exercise_by_exercise_type[exercise_type] = exercise_count

        return max_num_exercise_by_exercise_type

    @classmethod
    def _get_step_setting_from_query(cls, result: QSqlQuery) -> StepSetting:
        return StepSetting(
            step_setting_id=result.value('step_setting_id'), step_type=result.value('step_setting_type'),
            description=result.value('step_setting_description'), is_active=bool(result.value('step_setting_is_active'))
        )

    @classmethod
    def _get_exercise_setting_from_query(cls, result: QSqlQuery,
                                         max_num_exercise_by_exercise_type: dict) -> ExerciseSetting:
        return ExerciseSetting(
            exercise_setting_id=result.value('exercise_setting_id'),
            exercise_type=result.value('exercise_setting_exercise_type'),
            description=result.value('exercise_setting_description'),
            exercise_num=result.value('exercise_setting_exercise_num'),
            is_active=bool(result.value('exercise_setting_is_active')),
            max_exercise_num=max_num_exercise_by_exercise_type.get(result.value('exercise_setting_exercise_type'), 0),
            step_settings=[]
        )

    @classmethod
    def _get_topic_from_query(cls, result: QSqlQuery) -> Topic:
        identifier = result.value('topic_id')
        title = result.value('topic_title')
        description = result.value('topic_description')
        return Topic.create_topic(identifier=identifier, title=title, description=description, exercise_settings=[])

    @classmethod
    def save_topic_configuration(cls, topic: Topic):
        for exercise_setting in topic.exercise_settings:
            DatabaseAccessSingleton.execute_save_exercise_setting(topic_id=topic.id, exercise_setting=exercise_setting)

    @classmethod
    def get_resume_exercises(cls) -> defaultdict:
        result = DatabaseAccessSingleton.get_resume_result()

        resume_by_step_type = defaultdict(list)

        while result.next():
            step_type = result.value('step_type')
            exercise_id = result.value('exercise_id')
            resume = Resume(resume_id=result.value('id'), is_correct=bool(result.value('is_correct')),
                            step_type=step_type, response=result.value('response'),
                            exercise_id=exercise_id, graph_id=result.value('graph_id'))
            resume_by_step_type[step_type].append(resume)
        return resume_by_step_type

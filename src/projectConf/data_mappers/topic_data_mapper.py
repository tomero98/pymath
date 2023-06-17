from PyQt5.QtSql import QSqlQuery

from ..models import Topic, StepSetting, ExerciseSetting


class TopicDataMapper:
    @classmethod
    def get_topics(cls):
        max_num_exercise_by_exercise_type = cls._get_max_num_exercise_by_exercise_type()

        query = cls._get_topic_query()
        result = QSqlQuery()
        result.exec(query)

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
        query = cls._get_max_num_exercise_query()
        result = QSqlQuery()
        result.exec(query)

        max_num_exercise_by_exercise_type = {}
        while result.next():
            exercise_type = result.value('exercise_type')
            exercise_count = result.value('exercise_count')
            max_num_exercise_by_exercise_type[exercise_type] = exercise_count

        return max_num_exercise_by_exercise_type

    @classmethod
    def _get_max_num_exercise_query(cls) -> str:
        return """
            SELECT exercise_type, COUNT(*) AS exercise_count FROM exercises GROUP BY exercise_type
        """

    @staticmethod
    def _get_topic_query() -> str:
        return """
            SELECT topics.id                       AS topic_id,
                   topics.title                    AS topic_title,
                   topics.description              AS topic_description,
                   topics.first_time               AS topic_first_time,
                   exercise_settings.id            AS exercise_setting_id,
                   exercise_settings.exercise_type AS exercise_setting_exercise_type,
                   exercise_settings.description   AS exercise_setting_description,
                   exercise_settings.exercise_num  AS exercise_setting_exercise_num,
                   exercise_settings.is_active     AS exercise_setting_is_active,
                   step_settings.id                AS step_setting_id,
                   step_settings.step_type         AS step_setting_type,
                   step_settings.description       AS step_setting_description,
                   step_settings.is_active         AS step_setting_is_active
            FROM topics
            INNER JOIN exercise_settings ON topics.id = exercise_settings.topic_id
            INNER JOIN step_settings ON step_settings.exercise_setting_id = exercise_settings.id;
        """

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
        first_time = bool(result.value('topic_first_time'))
        return Topic.create_topic(identifier=identifier, title=title, description=description, first_time=first_time,
                                  exercise_settings=[])

    @classmethod
    def save_topic_configuration(cls, topic: Topic):
        for exercise_setting in topic.exercise_settings:
            cls._execute_save_exercise_setting(topic_id=topic.id, exercise_setting=exercise_setting)

    @classmethod
    def _execute_save_exercise_setting(cls, topic_id: int, exercise_setting: ExerciseSetting):
        sql_query = QSqlQuery()
        sql_query.prepare(
            """
            UPDATE exercise_settings
                SET exercise_num = :exercise_num,
                    is_active = :is_active
                WHERE topic_id = :topic_id AND exercise_type = :exercise_type
            """
        )
        sql_query.bindValue(':exercise_num', exercise_setting.exercise_num)
        sql_query.bindValue(':is_active', int(exercise_setting.is_active))
        sql_query.bindValue(':topic_id', topic_id)
        sql_query.bindValue(':exercise_type', exercise_setting.exercise_type)
        sql_query.exec()

        for step_setting in exercise_setting.step_settings:
            sql_query = QSqlQuery()
            sql_query.prepare(
                """
                UPDATE step_settings
                    SET is_active = :is_active
                    WHERE exercise_setting_id = :exercise_setting_id AND step_type = :step_type
                """
            )
            sql_query.bindValue(':is_active', int(step_setting.is_active))
            sql_query.bindValue(':exercise_setting_id', exercise_setting.id)
            sql_query.bindValue(':step_type', step_setting.step_type)
            sql_query.exec()

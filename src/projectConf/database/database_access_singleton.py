import os
import sys

from PyQt5.QtSql import QSqlDatabase, QSqlQuery

from .database_creator import DatabaseCreator
from ..models import ExerciseSetting


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DatabaseAccessSingleton(metaclass=Singleton):
    @staticmethod
    def setup_database():
        database_name = 'project.db'
        database = QSqlDatabase.addDatabase('QSQLITE')
        database.setDatabaseName(database_name)

        is_database_created = os.path.isfile(database_name)

        if not database.open():
            print("Database Error: %s" % database.lastError().databaseText())
            sys.exit(1)

        if not is_database_created:
            database_creator = DatabaseCreator()
            database_creator.create_database()

    @classmethod
    def get_max_nums_exercise_result(cls):
        query = cls._get_max_num_exercise_query()
        result = QSqlQuery()
        result.exec(query)
        return result

    @classmethod
    def _get_max_num_exercise_query(cls) -> str:
        return """
            SELECT exercise_type, COUNT(*) AS exercise_count FROM exercises GROUP BY exercise_type
        """

    @classmethod
    def get_topics_result(cls):
        query = cls._get_topic_query()
        result = QSqlQuery()
        result.exec(query)
        return result

    @staticmethod
    def _get_topic_query() -> str:
        return """
            SELECT topics.id                       AS topic_id,
                   topics.title                    AS topic_title,
                   topics.description              AS topic_description,
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
            INNER JOIN step_settings ON step_settings.exercise_setting_id = exercise_settings.id
            ORDER BY topics.topic_order
        """

    @classmethod
    def execute_save_exercise_setting(cls, topic_id: int, exercise_setting: ExerciseSetting):
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

    @classmethod
    def get_resume_result(cls):
        query = cls._get_resume_query()
        result = QSqlQuery()
        result.exec(query)
        return result

    @classmethod
    def _get_resume_query(cls) -> str:
        return """
            SELECT * FROM exercise_resumes
        """

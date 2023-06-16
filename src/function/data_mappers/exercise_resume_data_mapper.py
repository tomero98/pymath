from PyQt5.QtSql import QSqlQuery

from ..models import ExerciseResume
from ..models.enums import ResumeState


class ExerciseResumeDataMapper:
    @classmethod
    def save_resume_state(cls, resume: ExerciseResume):
        cls._execute_save_resume_state(resume=resume)

    @classmethod
    def _execute_save_resume_state(cls, resume: ExerciseResume):
        sql_query = QSqlQuery()
        sql_query.prepare(
            """
            INSERT INTO exercise_resumes (is_correct, step_type, exercise_id, graph_id, response) VALUES (?, ?, ?, ?, ?)
            """
        )

        is_correct = resume.resume_state == ResumeState.success
        sql_query.addBindValue(is_correct)
        sql_query.addBindValue(resume.step_type.value)
        sql_query.addBindValue(resume.exercise_id)
        sql_query.addBindValue(resume.function_id)
        sql_query.addBindValue(resume.response)
        sql_query.exec()

from typing import List

from .exercise_setting import ExerciseSetting


class Topic:
    def __init__(self, identifier: int, title: str, description: str, exercise_settings: List[ExerciseSetting]):
        self.id = identifier
        self.title = title
        self.description = description
        self.exercise_settings = exercise_settings

    @classmethod
    def create_topic(cls, identifier: int, title: str, description: str, exercise_settings: List[ExerciseSetting]):
        return cls(identifier=identifier, title=title, description=description, exercise_settings=exercise_settings)

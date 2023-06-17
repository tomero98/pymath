from typing import List

from .exercise_setting import ExerciseSetting


class Topic:
    def __init__(self, identifier: int, title: str, description: str, first_time: int,
                 exercise_settings: List[ExerciseSetting]):
        self.id = identifier
        self.title = title
        self.description = description
        self.first_time = first_time
        self.exercise_settings = exercise_settings

    @classmethod
    def create_topic(cls, identifier: int, title: str, description: str, first_time: int,
                     exercise_settings: List[ExerciseSetting]):
        return cls(identifier=identifier, title=title, description=description, first_time=first_time,
                   exercise_settings=exercise_settings)

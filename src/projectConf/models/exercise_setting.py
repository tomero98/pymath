from typing import List

from .step_setting import StepSetting


class ExerciseSetting:
    def __init__(self, exercise_setting_id: int, exercise_type: str, description: str, exercise_num: int,
                 is_active: bool, max_exercise_num: int, step_settings: List[StepSetting]):
        self.id = exercise_setting_id
        self.exercise_type = exercise_type
        self.description = description
        self.exercise_num = exercise_num
        self.max_exercise_num = max_exercise_num
        self.is_active = is_active
        self.step_settings = step_settings

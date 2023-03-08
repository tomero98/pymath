from .enums.step_type import StepType
from .enums.resume_state import ResumeState


class ExerciseResume:
    def __init__(self, resume_state: ResumeState, response, show_help: bool, exercise_id: int,
                 step_type: StepType, graph_id: int):
        self.resume_state = resume_state
        self.response = response
        self.show_help = show_help
        self.exercise_id = exercise_id
        self.step_type = step_type
        self.graph_id = graph_id

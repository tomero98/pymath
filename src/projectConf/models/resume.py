class Resume:
    def __init__(self, resume_id: int, is_correct: bool, step_type: str, response: str, exercise_id: int,
                 graph_id: int):
        self.id = resume_id
        self.is_correct = is_correct
        self.step_type = step_type
        self.response = response
        self.exercise_id = exercise_id
        self.graph_id = graph_id

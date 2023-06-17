class StepSetting:
    def __init__(self, step_setting_id: int, step_type: str, description: str, is_active: bool):
        self.id = step_setting_id
        self.step_type = step_type
        self.description = description
        self.is_active = is_active

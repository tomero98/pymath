from ..models import StepInfoData
from ..models.enums.step_type import StepType


class StepInfoDataMapper:
    def get_step_info_data(self, step_type: StepType) -> StepInfoData:
        step_info_data = None
        if step_type == StepType.inverse_concept_exercise:
            step_info_data = self._get_inverse_concept_info_data()
        elif step_type == StepType.selection_inverse_exercise:
            step_info_data = self._get_selection_inverse_info_data()
        elif step_type == StepType.delimited_inverse_exercise:
            step_info_data = self._get_delimited_inverse_info_data()
        elif step_type == StepType.indicate_domain_exercise:
            step_info_data = self._get_indicate_domain_info_data()
        elif step_type == StepType.indicate_range_exercise:
            step_info_data = self._get_indicate_range_info_data()
        elif step_type == StepType.indicate_elementary_exercise:
            step_info_data = self._get_indicate_elementary_exercise_info_data()
        elif step_type == StepType.indicate_elementary_shift_exercise:
            step_info_data = self._get_indicate_elementary_shift_exercise_info_data()
        elif step_type == StepType.maximum_minimum_exercise:
            step_info_data = self._get_maximum_minimum_info_data()
        if step_info_data:
            return step_info_data

    def _get_inverse_concept_info_data(self) -> StepInfoData:
        info_list = []
        return StepInfoData(video_name='inverse_concept_info_data.mp4', info_list=info_list)

    def _get_selection_inverse_info_data(self) -> StepInfoData:
        info_list = []
        return StepInfoData(video_name='selection_inverse_info_data.mp4', info_list=info_list)

    def _get_delimited_inverse_info_data(self) -> StepInfoData:
        info_list = []
        return StepInfoData(video_name='delimited_inverse_info_data.mp4', info_list=info_list)

    def _get_indicate_elementary_exercise_info_data(self) -> StepInfoData:
        info_list = []
        return StepInfoData(video_name='indicate_elementary_exercise_info_data.mp4', info_list=info_list)

    def _get_indicate_elementary_shift_exercise_info_data(self) -> StepInfoData:
        info_list = []
        return StepInfoData(video_name='indicate_elementary_shift_exercise_info_data.mp4', info_list=info_list)

    def _get_indicate_domain_info_data(self) -> StepInfoData:
        info_list = []
        return StepInfoData(video_name='indicate_domain_info', info_list=info_list)

    def _get_indicate_range_info_data(self) -> StepInfoData:
        info_list = []
        return StepInfoData(video_name='indicate_range_info', info_list=info_list)

    def _get_maximum_minimum_info_data(self)-> StepInfoData:
        info_list = []
        return StepInfoData(video_name='maximum_minimum_info_data.mp4', info_list=info_list)

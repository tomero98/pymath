from enum import Enum


class StepType(Enum):
    inverse_concept_exercise = 'ConceptInverseExercise'
    selection_inverse_exercise = 'SelectionInverseExercise'
    delimited_inverse_exercise = 'DelimitedInverseExercise'

    indicate_domain_exercise = 'IndicateDomainExercise'
    indicate_range_exercise = 'IndicateRangeExercise'

    indicate_elementary_exercise = 'IndicateElementaryExercise'
    indicate_elementary_shift_exercise = 'IndicateElementaryShiftExercise'

    maximum_minimum_exercise = 'MaximumMinimumExercise'

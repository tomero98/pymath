from enum import Enum


class InverseStepType(Enum):
    boolean_inverse_exercise = 'ConceptInverseExercise'
    selection_inverse_exercise = 'SelectionInverseExercise'
    delimited_inverse_exercise = 'DelimitedInverseExercise'
    indicate_domain_exercise = 'IndicateDomainExercise'
    indicate_range_exercise = 'IndicateRangeExercise'
    indicate_bounded_range_exercise = 'IndicateBoundedRangeExercise'
    indicate_elementary_exercise = 'IndicateElementaryExercise'
    maximum_relative_exercise = 'MaximumRelativeExercise'
    maximum_absolute_exercise = 'MaximumAbsoluteExercise'
    minimum_relative_exercise = 'MinimumRelativeExercise'
    minimum_absolute_exercise = 'MinimumAbsoluteExercise'

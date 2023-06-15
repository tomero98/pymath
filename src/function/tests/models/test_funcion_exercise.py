from unittest import TestCase
from unittest.mock import Mock

from ...models import Function, FunctionExercise


class TestFunctionExercise(TestCase):
    def test_validate_domain_expression__domain_expression_match(self):
        function_exercise = FunctionExercise(identifier=0, exercise_type='', title='', plot_range=(-5, 5),
                                             exercise_order=0, functions=[], steps=[])
        function_exercise.get_domain_expression = Mock(return_value='(3, 5]')
        self.assertTrue(function_exercise.validate_domain_expression(user_domain_input='(3, 5]'))

        function_exercise.get_domain_expression = Mock(return_value='(3, 5] U (6, 9)')
        self.assertTrue(function_exercise.validate_domain_expression(user_domain_input='(6, 9) U (3, 5]'))

    def test_validate_domain_expression__values_match(self):
        function_one = Function(function_id=0, expression='x', x_values_range=(2, 3), is_main_graphic=True,
                                domain='(4, 5]')
        function_two = Function(function_id=0, expression='x', x_values_range=(4, 5), is_main_graphic=True,
                                domain='[2, 3)')
        function_exercise = FunctionExercise(identifier=0, exercise_type='', title='', plot_range=(-5, 5),
                                             exercise_order=0, functions=[function_one, function_two], steps=[])
        result, set_result_wrong, set_result_missed = function_exercise.validate_domain_expression('[2, 3) U (4, 5]')
        self.assertTrue(result)
        self.assertEqual(set(), set_result_wrong)
        self.assertEqual(set(), set_result_missed)

        function_one.domain = '[3, +inf)'
        function_two.domain = '(-inf, 0]'
        result, set_result_wrong, set_result_missed = function_exercise.validate_domain_expression(
            '(-inf, 0] U [3, +inf)'
        )
        self.assertTrue(result)
        self.assertEqual(set(), set_result_wrong)
        self.assertEqual(set(), set_result_missed)

    def test_validate_domain_expression__values_no_match(self):
        function_one = Function(function_id=0, expression='x', x_values_range=(2, 3), is_main_graphic=True,
                                domain='[4, 5)')
        function_two = Function(function_id=0, expression='x', x_values_range=(4, 5), is_main_graphic=True,
                                domain='(2, 3]')
        function_exercise = FunctionExercise(identifier=0, exercise_type='', title='', plot_range=(-5, 5),
                                             exercise_order=0, functions=[function_one, function_two], steps=[])
        result, set_result_wrong, set_result_missed = function_exercise.validate_domain_expression('[2, 3) U (4, 5]')
        self.assertFalse(result)
        self.assertEqual({2, 5}, set_result_wrong)
        self.assertEqual({3, 4}, set_result_missed)

        function_one.domain = '[3, +inf)'
        function_exercise.functions.pop()
        result, set_result_wrong, set_result_missed = function_exercise.validate_domain_expression('(-inf, 4]')

        self.assertFalse(result)
        self.assertEqual(set([num / 10 for num in range(-5 * 10, 3 * 10 + 1, 1)][:-1]), set_result_wrong)
        self.assertEqual(set([num / 10 for num in range(4 * 10, 5 * 10 + 1, 1)][1:]), set_result_missed)

    def test_get_domain_expression(self):
        function_one = Function(function_id=0, expression='', x_values_range=tuple(), is_main_graphic=True,
                                domain='(4, +inf)')
        function_exercise = FunctionExercise(identifier=0, exercise_type='', title='', plot_range=(-5, 5),
                                             exercise_order=0, functions=[function_one], steps=[])
        self.assertEqual('(4, +inf)', function_exercise.get_domain_expression())

        function_two = Function(function_id=0, expression='', x_values_range=tuple(), is_main_graphic=True,
                                domain='(-inf, 2)')
        function_exercise.functions = [function_one, function_two]
        self.assertEqual('(4, +inf) U (-inf, 2)', function_exercise.get_domain_expression())
        
    def test_get_num_set_from_domain_expression(self):
        function_exercise = FunctionExercise(identifier=0, exercise_type='', title='', plot_range=(-5, 5),
                                             exercise_order=0, functions=[], steps=[])
        domain_set = function_exercise.get_num_set_from_domain_expression('(0, +inf)')
        expected_set = set([num / 10 for num in range(0 * 10, 5 * 10 + 1, 1)][1:])
        self.assertEqual(expected_set, domain_set)

        domain_set = function_exercise.get_num_set_from_domain_expression('[-1, 0]')
        expected_set = set([num / 10 for num in range(-1 * 10, 0 * 10 + 1, 1)])
        self.assertEqual(expected_set, domain_set)

        domain_set = function_exercise.get_num_set_from_domain_expression('(-inf, -2)')
        expected_set = set([num / 10 for num in range(-5 * 10, -2 * 10 + 1, 1)][:-1])
        self.assertEqual(expected_set, domain_set)
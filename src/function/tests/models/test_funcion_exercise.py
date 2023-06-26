from unittest import TestCase
from unittest.mock import Mock

from ...models import Function, FunctionExercise, Point


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

    def test_get_maximum_minimum_points__1(self):
        function_exercise = FunctionExercise(identifier=0, exercise_type='', title='', plot_range=(-3, 3),
                                             exercise_order=0, functions=[], steps=[])
        function = Function(function_id=0, expression='x', x_values_range=(-1, 1), is_main_graphic=True,
                            domain='(-1, 1]')
        function.setup_data((-2, 2))
        function_exercise.functions.append(function)
        max_min_points_dict = function_exercise.get_maximum_minimum_points()
        expected_dict = {
            'máximo absoluto': [(1, 1)],
            'máximo relativo': None,
            'mínimo absoluto': None,
            'mínimo relativo': None,
        }
        self.assertEqual(expected_dict, max_min_points_dict)

    def test_get_maximum_minimum_points__2(self):
        function_exercise = FunctionExercise(identifier=0, exercise_type='', title='', plot_range=(-3, 3),
                                             exercise_order=0, functions=[], steps=[])
        function = Function(function_id=0, expression='x', x_values_range=(-3, 3), is_main_graphic=True,
                            domain='(-inf, +inf)')
        function.setup_data((-2, 2))
        function_exercise.functions.append(function)
        max_min_points_dict = function_exercise.get_maximum_minimum_points()
        expected_dict = {
            'máximo absoluto': None,
            'máximo relativo': None,
            'mínimo absoluto': None,
            'mínimo relativo': None,
        }
        self.assertEqual(expected_dict, max_min_points_dict)
    def test_get_maximum_minimum_points__3(self):
        function_exercise = FunctionExercise(identifier=0, exercise_type='', title='', plot_range=(-3, 3),
                                             exercise_order=0, functions=[], steps=[])
        function = Function(function_id=0, expression='(x)**2', x_values_range=(-3, 3), is_main_graphic=True,
                            domain='(-3, 3)')
        function.setup_data((-3, 3))
        function_exercise.functions.append(function)
        max_min_points_dict = function_exercise.get_maximum_minimum_points()
        expected_dict = {
            'máximo absoluto': None,
            'máximo relativo': None,
            'mínimo absoluto': [(0, 0)],
            'mínimo relativo': None,
        }
        self.assertEqual(expected_dict, max_min_points_dict)

    def test_get_maximum_minimum_points__4(self):
        function_exercise = FunctionExercise(identifier=0, exercise_type='', title='', plot_range=(-3, 3),
                                             exercise_order=0, functions=[], steps=[])
        function = Function(function_id=0, expression='(x)**2', x_values_range=(-3, 0), is_main_graphic=True,
                            domain='(-3, 0)')
        function.setup_data((-3, 3))
        function_exercise.functions.append(function)
        max_min_points_dict = function_exercise.get_maximum_minimum_points()
        expected_dict = {
            'máximo absoluto': None,
            'máximo relativo': None,
            'mínimo absoluto': None,
            'mínimo relativo': None,
        }
        self.assertEqual(expected_dict, max_min_points_dict)

    def test_get_maximum_minimum_points__5(self):
        function_exercise = FunctionExercise(identifier=0, exercise_type='', title='', plot_range=(-3, 3),
                                             exercise_order=0, functions=[], steps=[])
        function = Function(function_id=0, expression='(x)**2', x_values_range=(-3, 0), is_main_graphic=True,
                            domain='(-3, 0)')
        function.setup_data((-3, 3))
        function_exercise.functions.append(function)
        function = Function(function_id=0, expression='x', x_values_range=(0, 1), is_main_graphic=True,
                            domain='[0, 1]')
        function.setup_data((-3, 3))
        function_exercise.functions.append(function)
        max_min_points_dict = function_exercise.get_maximum_minimum_points()
        expected_dict = {
            'máximo absoluto': None,
            'máximo relativo': [(1, 1)],
            'mínimo absoluto': [(0, 0)],
            'mínimo relativo': None,
        }
        self.assertEqual(expected_dict, max_min_points_dict)

    def test_get_maximum_minimum_points__6(self):
        function_exercise = FunctionExercise(identifier=0, exercise_type='', title='', plot_range=(-3, 3),
                                             exercise_order=0, functions=[], steps=[])
        function = Function(function_id=0, expression='(x)**2', x_values_range=(-3, 0), is_main_graphic=True,
                            domain='(-3, 0)')
        function.setup_data((-3, 3))
        function_exercise.functions.append(function)
        function = Function(function_id=0, expression='x', x_values_range=(0, 1), is_main_graphic=True,
                            domain='(0, 1]')
        function.setup_data((-3, 3))
        function_exercise.exercise_points.append(Point(0, 3, True))
        function_exercise.functions.append(function)
        max_min_points_dict = function_exercise.get_maximum_minimum_points()
        expected_dict = {
            'máximo absoluto': None,
            'máximo relativo': [(0, 3), (1, 1)],
            'mínimo absoluto': None,
            'mínimo relativo': None,
        }
        self.assertEqual(expected_dict, max_min_points_dict)

    def test_get_maximum_minimum_points__7(self):
        function_exercise = FunctionExercise(identifier=0, exercise_type='', title='', plot_range=(-3, 3),
                                             exercise_order=0, functions=[], steps=[])
        function = Function(function_id=0, expression='(x)**2', x_values_range=(-3, 0), is_main_graphic=True,
                            domain='(-3, 0)')
        function.setup_data((-3, 3))
        function_exercise.functions.append(function)
        function = Function(function_id=0, expression='x-1', x_values_range=(1, 2), is_main_graphic=True,
                            domain='[1, 2)')
        function.setup_data((-3, 3))
        function_exercise.exercise_points.append(Point(0, 3, True))
        function_exercise.functions.append(function)
        max_min_points_dict = function_exercise.get_maximum_minimum_points()
        expected_dict = {
            'máximo absoluto': None,
            'máximo relativo': [(0, 3)],
            'mínimo absoluto': [(1, 0)],
            'mínimo relativo': None,
        }
        self.assertEqual(expected_dict, max_min_points_dict)

    def test_get_maximum_minimum_points__constant_function(self):
        function_exercise = FunctionExercise(identifier=0, exercise_type='', title='', plot_range=(-3, 3),
                                             exercise_order=0, functions=[], steps=[])
        function = Function(function_id=0, expression='2', x_values_range=(-1, 0), is_main_graphic=True,
                            domain='(-1, 0]')
        function.setup_data((-3, 3))
        function_exercise.functions.append(function)

        max_min_points_dict = function_exercise.get_maximum_minimum_points()
        expected_dict = {
            'máximo absoluto': [(num / 100, 2) for num in range(-1 * 100, 0 * 100 + 1, 1)][1:],
            'máximo relativo': None,
            'mínimo absoluto': [(num / 100, 2) for num in range(-1 * 100, 0 * 100 + 1, 1)][1:],
            'mínimo relativo': None,
        }
        self.assertEqual(expected_dict, max_min_points_dict)

    def test_get_maximum_minimum_points__all_functions__with_shift(self):
        function_exercise = FunctionExercise(identifier=0, exercise_type='', title='', plot_range=(-3, 3),
                                             exercise_order=0, functions=[], steps=[])
        function = Function(function_id=0, expression='(x)**2', x_values_range=(-3, 0), is_main_graphic=True,
                            domain='(-3, 0)')
        function.setup_data((-3, 3))
        function_exercise.functions.append(function)
        function = Function(function_id=0, expression='x-1', x_values_range=(1, 2), is_main_graphic=True,
                            domain='(1, 2]')
        function.setup_data((-3, 3))
        function_exercise.functions.append(function)
        function = Function(function_id=0, expression='1', x_values_range=(3, 4), is_main_graphic=True,
                            domain='[3, 4)')
        function.setup_data((-4, 4))
        function_exercise.exercise_points.append(Point(0, -3, True))
        function_exercise.functions.append(function)
        max_min_points_dict = function_exercise.get_maximum_minimum_points()

        constant_values = [(num / 100, 1) for num in range(3 * 100, 4 * 100 + 1, 1)]
        expected_dict = {
            'máximo absoluto': None,
            'máximo relativo': [(2, 1), *constant_values[:-1]],
            'mínimo absoluto': [(0, -3)],
            'mínimo relativo': constant_values[:-1],
        }
        self.assertEqual(expected_dict, max_min_points_dict)

    def test_get_maximum_minimum_points__all_functions__with_no_shifts(self):
        function_exercise = FunctionExercise(identifier=0, exercise_type='', title='', plot_range=(-3, 3),
                                             exercise_order=0, functions=[], steps=[])
        function = Function(function_id=0, expression='(x)**2', x_values_range=(-3, 0), is_main_graphic=True,
                            domain='(-3, 0)')
        function.setup_data((-3, 3))
        function_exercise.functions.append(function)
        function = Function(function_id=0, expression='x-1', x_values_range=(1, 2), is_main_graphic=True,
                            domain='(1, 2]')
        function.setup_data((-3, 3))
        function_exercise.functions.append(function)
        function = Function(function_id=0, expression='1', x_values_range=(2, 3), is_main_graphic=True,
                            domain='[3, 4)')
        function.setup_data((-4, 4))
        function_exercise.exercise_points.append(Point(0, -3, True))
        function_exercise.functions.append(function)
        max_min_points_dict = function_exercise.get_maximum_minimum_points()

        constant_values = [(num / 100, 1) for num in range(2 * 100, 3 * 100 + 1, 1)]
        expected_dict = {
            'máximo absoluto': None,
            'máximo relativo': [(2, 1), *constant_values[:-1]],
            'mínimo absoluto': [(0, -3)],
            'mínimo relativo': constant_values[1:-1],
        }
        self.assertEqual(expected_dict, max_min_points_dict)
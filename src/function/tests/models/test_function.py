from unittest import TestCase

from ...models import Function


class TestFunction(TestCase):
    def test_get_domain__no_asymptotes(self):
        function = Function(function_id=0, expression='', x_values_range=tuple(), is_main_graphic=True,
                            domain='(-inf, +inf)')
        domain = function.get_domain('(-inf, +inf)')
        self.assertEqual('(-inf, +inf)', domain)

    def test_get_domain__asymptotes(self):
        function = Function(function_id=0, expression='', x_values_range=tuple(), is_main_graphic=True,
                            domain='(-inf, 5]')
        function.vertical_asymptotes = [-2, 1, 3]
        domain = function.get_domain('(-inf, 5]')
        self.assertEqual('(-inf, -2) U (-2, 1) U (1, 3) U (3, 5]', domain)

        function = Function(function_id=0, expression='', x_values_range=tuple(), is_main_graphic=True,
                            domain='(-inf, 5]')
        function.vertical_asymptotes = [-2]
        domain = function.get_domain('(-inf, 5]')
        self.assertEqual('(-inf, -2) U (-2, 5]', domain)

    def test_get_range_expression__no_asymptotes(self):
        function = Function(function_id=0, expression='x', x_values_range=(-1, 1), domain='(-1, 1]',
                            is_main_graphic=True)
        function.x_values, function.y_values = function.get_points()
        function.horizontal_asymptotes = []
        y_range = function.get_range_expression(plot_range=(-3, 3))
        self.assertEqual('(-1.0, 1.0]', y_range)

        function = Function(function_id=0, expression='x', x_values_range=(-1, 1), domain='[-1, 1)',
                            is_main_graphic=True)
        function.x_values, function.y_values = function.get_points()
        function.horizontal_asymptotes = []
        y_range = function.get_range_expression(plot_range=(-3, 3))
        self.assertEqual('[-1.0, 1.0)', y_range)

        function = Function(function_id=0, expression='x', x_values_range=(-1, 1), domain='(-inf, +inf)',
                            is_main_graphic=True)
        function.x_values, function.y_values = function.get_points()
        function.horizontal_asymptotes = []
        y_range = function.get_range_expression(plot_range=(-3, 3))
        self.assertEqual('[-1.0, 1.0]', y_range)

        function = Function(function_id=0, expression='-x', x_values_range=(-1, 1), domain='(-1, 1]',
                            is_main_graphic=True)
        function.x_values, function.y_values = function.get_points()
        function.horizontal_asymptotes = []
        y_range = function.get_range_expression(plot_range=(-3, 3))
        self.assertEqual('[-1.0, 1.0)', y_range)

        function = Function(function_id=0, expression='-x', x_values_range=(-1, 1), domain='[-1, 1)',
                            is_main_graphic=True)
        function.x_values, function.y_values = function.get_points()
        function.horizontal_asymptotes = []
        y_range = function.get_range_expression(plot_range=(-3, 3))
        self.assertEqual('(-1.0, 1.0]', y_range)

        function = Function(function_id=0, expression='(x)**3', x_values_range=(-2, 2), domain='(-2, 2)',
                            is_main_graphic=True)
        function.x_values, function.y_values = function.get_points()
        function.horizontal_asymptotes = []
        y_range = function.get_range_expression(plot_range=(-3, 3))
        self.assertEqual('(-inf, +inf)', y_range)

    def test_get_range_expression__asymptotes(self):
        function = Function(function_id=0, expression='x', x_values_range=(-1, 1), domain='(-1, 1]',
                            is_main_graphic=True)
        function.x_values, function.y_values = function.get_points()
        function.horizontal_asymptotes = [0]
        y_range = function.get_range_expression(plot_range=(-3, 3))
        self.assertEqual('(-1.0, 0) U (0, 1.0]', y_range)

    def test_get_horizontal_asymptotes(self):
        function = Function(function_id=0, expression='x/(x+1)', x_values_range=tuple(), is_main_graphic=True,
                            domain='(-inf, 5]')
        asymptotes = function.get_horizontal_asymptotes()
        self.assertEqual([1], asymptotes)

        function = Function(function_id=0, expression='2/(1+math.e**x)', x_values_range=tuple(), is_main_graphic=True,
                            domain='(-inf, 5]')
        asymptotes = function.get_horizontal_asymptotes()
        self.assertEqual([2, 0], asymptotes)

    def test_get_horizontal_asymptotes__no_asymptotes(self):
        function = Function(function_id=0, expression='x', x_values_range=tuple(), is_main_graphic=True,
                            domain='(-inf, 5]')
        asymptotes = function.get_horizontal_asymptotes()
        self.assertEqual([], asymptotes)

    def test_get_horizontal_asymptotes__no_asymptotes__cos_sin(self):
        function = Function(function_id=0, expression='cos(x)', x_values_range=tuple(), is_main_graphic=True,
                            domain='(-inf, 5]')
        asymptotes = function.get_horizontal_asymptotes()
        self.assertEqual([], asymptotes)

        function.expression = 'sin(x)'
        asymptotes = function.get_horizontal_asymptotes()
        self.assertEqual([], asymptotes)

    def test_get_maximum_minimum_points(self):
        function = Function(function_id=0, expression='x**2', x_values_range=tuple(), is_main_graphic=True,
                            domain='(-inf, 5]')
        maximum_values, maximum_absolute, minimum_values, minimum_absolute = function.get_maximum_minimum_points(
            plot_range=(-5, 5))
        a=8

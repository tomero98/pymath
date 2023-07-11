from typing import List

from ..models import HelpStep, Function, FunctionExercise, HelpData, Point
from ..models.enums.step_type import StepType


class HelpDataMapper:
    def __init__(self, exercise: FunctionExercise):
        self._exercise = exercise

    def get_help_data(self, step_type: StepType) -> List[HelpData]:
        help_data_list = []
        if step_type == StepType.inverse_concept_exercise:
            help_data_list = self._get_inverse_concept_help()
        elif step_type == StepType.selection_inverse_exercise:
            help_data_list = self._get_selection_inverse_help()
        elif step_type == StepType.delimited_inverse_exercise:
            help_data_list = self._get_delimited_inverse_help()

        elif step_type == StepType.maximum_minimum_exercise:
            help_data_list = self._get_maximum_minimum_help()

        elif step_type == StepType.indicate_domain_exercise:
            help_data_list = self._get_indicate_domain_help()
        elif step_type == StepType.indicate_range_exercise:
            help_data_list = self._get_indicate_range_help()

        elif step_type == StepType.indicate_elementary_shift_exercise:
            help_data_list = self._get_indicate_elementary_shift_exercise_help()
        return help_data_list

    def _get_inverse_concept_help(self) -> List[HelpData]:
        return [self._get_help_data_inverse_concept_help()]

    def _get_help_data_inverse_concept_help(self) -> HelpData:
        first_step = self._get_first_step_inverse_concept_help()
        function = Function(function_id=0, expression='(x)**2', x_values_range=(-4, 4), is_main_graphic=True)
        function.setup_data(plot_range=(-5, 5))
        text = '¿Se repiten imágenes?'
        return HelpData(order=0, functions=[function], help_steps=[first_step],
                        title='Apuntes sobre funciones inversas', text=text)

    def _get_first_step_inverse_concept_help(self) -> HelpStep:
        function_one = Function(function_id=0, expression='1', x_values_range=(-5, 5), is_main_graphic=False)
        function_one.setup_data(plot_range=(-5, 5))

        function_two = Function(function_id=0, expression='4', x_values_range=(-5, 5), is_main_graphic=False)
        function_two.setup_data(plot_range=(-5, 5))
        text = 'Si se repiten imágenes la función no tiene inversa para el dominio dado.'
        point_one = Point(x=1, y=1)
        point_two = Point(x=-1, y=1)
        point_three = Point(x=2, y=4)
        point_four = Point(x=-2, y=4)
        return HelpStep(order=0, functions=[function_one, function_two], text=text, function_color='blue',
                        point_color='red', points=[point_one, point_two, point_three, point_four])

    def _get_selection_inverse_help(self) -> List[HelpData]:
        return [self._get_help_data_selection_inverse_help()]

    def _get_help_data_selection_inverse_help(self) -> HelpData:
        function = Function(function_id=0, expression='(x)**3', x_values_range=(-4, 4), is_main_graphic=True)
        function.setup_data(plot_range=(-5, 5))
        first_step = self._get_first_step_selection_inverse_help()
        second_step = self._get_second_step_selection_inverse_help(function=function)
        return HelpData(order=0, functions=[function], help_steps=[first_step, second_step],
                        title='Apuntes sobre funciones inversas',
                        text='La función inversa es aquella que intercambia los valores de entrada de la función por '
                             'sus imágenes.')

    def _get_first_step_selection_inverse_help(self) -> HelpStep:
        function_two = Function(function_id=0, expression='x', x_values_range=(-5, 5), is_main_graphic=False)
        function_two.setup_data(plot_range=(-5, 5))
        text = 'Con la ayuda de la recta x=y podemos observar la relación entre los elementos de una función y su ' \
               'inversa, los valores de entrada de la función inversa son las imágenes de la función y viceversa.'
        return HelpStep(order=0, functions=[function_two], text=text, function_color='blue')

    def _get_second_step_selection_inverse_help(self, function: Function) -> HelpStep:
        function_one = Function(function_id=0, expression='1', x_values_range=(-4, 4), is_main_graphic=False,
                                is_invert_function=True)
        function_one.x_values = function.y_values
        function_one.y_values = function.x_values

        text = 'Con la ayuda de la recta x=y podemos observar la relación entre los elementos de una función y su ' \
               'inversa, los valores de entrada de la función inversa son las imágenes de la función y viceversa.'
        return HelpStep(order=0, functions=[function_one], text=text, function_color='green')

    def _get_delimited_inverse_help(self) -> List[HelpData]:
        return [self._get_help_data_delimited_inverse_help()]

    def _get_help_data_delimited_inverse_help(self) -> HelpData:
        function = Function(function_id=0, expression='(x)**2', x_values_range=(-4, 4), is_main_graphic=True)
        function.setup_data(plot_range=(-5, 5))
        first_step = self._get_first_step_delimited_inverse_help()
        return HelpData(order=0, functions=[function], help_steps=[first_step],
                        title='Apuntes sobre funciones inversas',
                        text='Si se repiten imágenes recortamos dominio para evitar repeticiones y así obtener una '
                             'función inversa para la función.')

    def _get_first_step_delimited_inverse_help(self) -> HelpStep:
        function_one = Function(function_id=0, expression='(x)**2', x_values_range=(0, 3), is_main_graphic=False)
        function_one.setup_data(plot_range=(-5, 5))
        function_one.x_values, function_one.y_values = function_one.y_values, function_one.x_values

        text = 'Ejemplo de dominio recortado, la función ahora sí tiene inversa.'
        return HelpStep(order=0, functions=[function_one], help_ranges=[(0, 5)], text=text, function_color='blue')

    def _get_indicate_elementary_shift_exercise_help(self) -> List[HelpData]:
        first_help_data = self._get_first_help_data_elementary_shift()
        second_help_data = self._get_second_help_data_elementary_shift()
        return [first_help_data, second_help_data]

    def _get_first_help_data_elementary_shift(self) -> HelpData:
        first_step = self._get_first_step_elementary_shift()
        second_step = self._get_second_step_elementary_shift()
        function = Function(function_id=0, expression='(x)**2', x_values_range=(-4, 4), is_main_graphic=True)
        function.setup_data(plot_range=(-5, 5))
        return HelpData(order=0, functions=[function], help_steps=[first_step, second_step],
                        title='Apuntes sobre desplazamientos en funciones',
                        text='Desplazamientos horizontales sobre f(x).')

    def _get_first_step_elementary_shift(self) -> HelpStep:
        function = Function(function_id=0, expression='(x + 1)**2', x_values_range=(-4, 4), is_main_graphic=False)
        function.setup_data(plot_range=(-5, 5))
        return HelpStep(order=0, functions=[function], text='Desplazamiento horizontal hacia la izquierda: f(x + 1).',
                        function_color='blue')

    def _get_second_step_elementary_shift(self) -> HelpStep:
        function = Function(function_id=0, expression='(x - 1)**2', x_values_range=(-4, 4), is_main_graphic=False)
        function.setup_data(plot_range=(-5, 5))
        return HelpStep(order=1, functions=[function],
                        text='Desplazamiento horizontal hacia la derecha: f(x - 1).',
                        function_color='purple')

    def _get_second_help_data_elementary_shift(self) -> HelpData:
        first_step = self._get_third_step_elementary_shift()
        second_step = self._get_fourth_step_elementary_shift()
        function = Function(function_id=0, expression='(x)**2', x_values_range=(-3, 3), is_main_graphic=True)
        function.setup_data(plot_range=(-5, 5))
        return HelpData(order=1, functions=[function], help_steps=[first_step, second_step],
                        title='Apuntes sobre desplazamientos en funciones',
                        text='Desplazamientos verticales sobre f(x).')

    def _get_third_step_elementary_shift(self) -> HelpStep:
        function = Function(function_id=0, expression='(x)**2 + 1', x_values_range=(-3, 3), is_main_graphic=False)
        function.setup_data(plot_range=(-5, 5))
        return HelpStep(order=0, functions=[function], text='Desplazamiento vertical hacia arriba: f(x) + 1.',
                        function_color='blue')

    def _get_fourth_step_elementary_shift(self) -> HelpStep:
        function = Function(function_id=0, expression='(x)**2 - 1', x_values_range=(-3, 3), is_main_graphic=False)
        function.setup_data(plot_range=(-5, 5))
        return HelpStep(order=1, functions=[function], text='Desplazamiento vertical hacia abajo: f(x) - 1.',
                        function_color='purple')

    def _get_indicate_domain_help(self) -> List[HelpData]:
        first_help_data = self._get_first_help_data_domain()
        return [first_help_data]

    def _get_first_help_data_domain(self) -> HelpData:
        function_one = Function(function_id=0, expression='(x)**2', x_values_range=(-2, 3), is_main_graphic=True,
                                domain='[-2, +inf)')
        function_one.setup_data(plot_range=(-5, 5))
        help_step_one = self._get_first_help_step_domain()
        return HelpData(order=0, title='Apuntes sobre el dominio de una función',
                        functions=[function_one], help_steps=[help_step_one],
                        text='El dominio de una función corresponde al conjunto de valores para los que la '
                             'función está definida.')

    def _get_first_help_step_domain(self) -> HelpStep:
        text = 'Para la gráfica mostrada, el dominio es [-2, inf) porque no vemos punto límite para la función por la ' \
               'derecha, así que nos podemos imaginar que continua infinitamente.'
        return HelpStep(order=0, functions=[], text=text, help_range_orientation='vertical', help_ranges=[(-2, 6)])

    def _get_indicate_range_help(self) -> List[HelpData]:
        first_help_data = self._get_first_help_data_range()
        return [first_help_data]

    def _get_first_help_data_range(self) -> HelpData:
        function_one = Function(function_id=0, expression='3', x_values_range=(-2, 3), is_main_graphic=True,
                                domain='[-2, +inf)')
        function_one.setup_data(plot_range=(-5, 5))
        help_step_one = self._get_first_help_step_range()
        return HelpData(order=0, title='Apuntes sobre el recorrido de una función',
                        functions=[function_one], help_steps=[help_step_one],
                        text='El recorrido de una función es el conjunto de valores que puede alcanzar la función.')

    def _get_first_help_step_range(self) -> HelpStep:
        text = 'Para la gráfica mostrada, el único valor alcanzado por la función es 3, el recorrido de esta ' \
               'función es {3}.'
        return HelpStep(order=0, functions=[], text=text, help_range_orientation='horizontal', help_ranges=[(3, 3)])

    def _get_maximum_minimum_help(self) -> List[HelpData]:
        first_help_data = self._get_help_maximum_range()
        second_help_data = self._get_help_constant_values()
        return [first_help_data, second_help_data]

    def _get_help_maximum_range(self) -> HelpData:
        function_one = Function(function_id=0, expression='(x)**2', x_values_range=(-2, 2), is_main_graphic=True,
                                domain='[-2, 2]')
        function_one.setup_data(plot_range=(-5, 5))
        help_step_one = self._get_first_help_step_maximum()
        return HelpData(order=0, title='Apuntes sobre máximos y mínimos de una función',
                        functions=[function_one], help_steps=[help_step_one],
                        text='¿Puede existir más de un máximo absoluto?')

    def _get_first_help_step_maximum(self) -> HelpStep:
        point_one = Point(x=2, y=4)
        point_two = Point(x=-2, y=4)
        text = 'Sí, ambos cumplen con la definición de máximo absoluto.'
        return HelpStep(order=0, functions=[], points=[point_one, point_two], text=text, point_color='red')

    def _get_help_constant_values(self) -> HelpData:
        function_one = Function(function_id=0, expression='2', x_values_range=(-2, 2), is_main_graphic=True,
                                domain='[-2, 2]')
        function_one.setup_data(plot_range=(-5, 5))

        help_step_one = self._get_first_help_constant_minimum()
        return HelpData(order=2, title='Apuntes sobre máximos y mínimos de una función',
                        functions=[function_one], help_steps=[help_step_one],
                        text='¿Y qué ocurre con las funciones constantes?')

    def _get_first_help_constant_minimum(self) -> HelpStep:
        function_one = Function(function_id=0, expression='2', x_values_range=(-2, 2), is_main_graphic=True,
                                domain='[-2, 2]')
        function_one.setup_data(plot_range=(-5, 5))
        text = 'Todos sus puntos definidos cumplen la definición de máximo y mínimo al mismo tiempo.'
        return HelpStep(order=0, functions=[function_one], text=text, function_color='orange')

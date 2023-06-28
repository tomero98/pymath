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

        # elif step_type == StepType.maximum_minimum_exercise:
        #     help_data_list = self._get_maximum_minimum_help()

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
        text = 'Dada una función biyectiva f(x) que relaciona elementos de un conjunto A con elementos de un conjunto ' \
               'B (A → B), se definirá su función inversa f⁻¹(x) como la función que realiza de forma inversa la ' \
               'asignación entre conjuntos A y B (B → A). Los valores del conjunto inicial de f(x) son los valores del ' \
               'conjunto imagen de f⁻¹(x) y los valores del conjunto imagen de f(x) son los valores del conjunto ' \
               'inicial de f⁻¹(x).'
        return HelpData(order=0, functions=[function], help_steps=[first_step],
                        title='Apuntes sobre funciones inversas', text=text)

    def _get_first_step_inverse_concept_help(self) -> HelpStep:
        function_one = Function(function_id=0, expression='1', x_values_range=(-5, 5), is_main_graphic=False)
        function_one.setup_data(plot_range=(-5, 5))

        function_two = Function(function_id=0, expression='4', x_values_range=(-5, 5), is_main_graphic=False)
        function_two.setup_data(plot_range=(-5, 5))
        text = 'Las funciones inversas son funciones biyectivas, cualquier par de elementos del conjunto inicial tiene ' \
               'imágenes distintas y el conjunto imagen coincide con el conjunto final. Las funciones constantes ' \
               'f(x)=1 y g(x)=4 muestran valores repetidos para un par de elementos del conjunto inicial, por ello ' \
               'la función mostrada no tiene inversa en este dominio.'
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
        first_step = self._get_first_step_selection_inverse_help(function=function)
        return HelpData(order=0, functions=[function], help_steps=[first_step],
                        title='Apuntes sobre funciones inversas',
                        text='La función inversa de f(x), f⁻¹(x), es aquella cuyos valores del conjunto inicial de f(x)'
                             ' son los valores del conjunto imagen de f⁻¹(x) y los valores del conjunto imagen de f(x)'
                             ' son los valores del conjunto inicial de f⁻¹(x).')

    def _get_first_step_selection_inverse_help(self, function: Function) -> HelpStep:
        function_one = Function(function_id=0, expression='1', x_values_range=(-4, 4), is_main_graphic=False,
                                is_invert_function=True)
        function_one.x_values = function.y_values
        function_one.y_values = function.x_values

        function_two = Function(function_id=0, expression='x', x_values_range=(-5, 5), is_main_graphic=False)
        function_two.setup_data(plot_range=(-5, 5))
        text = 'Con la ayuda de la función f(x)=y podemos observar la relación entre una función y su inversa, ' \
               'los valores de la función inversa son la reflexión de los valores de la función sobre f(x)=y.'
        return HelpStep(order=0, functions=[function_one, function_two], text=text, function_color='blue')

    def _get_delimited_inverse_help(self) -> List[HelpData]:
        return [self._get_help_data_delimited_inverse_help()]

    def _get_help_data_delimited_inverse_help(self) -> HelpData:
        function = Function(function_id=0, expression='(x)**2', x_values_range=(-4, 4), is_main_graphic=True)
        function.setup_data(plot_range=(-5, 5))
        first_step = self._get_first_step_delimited_inverse_help()
        return HelpData(order=0, functions=[function], help_steps=[first_step],
                        title='Apuntes sobre funciones inversas',
                        text='La restricción de dominio sobre una función permite obtener funciones inversas sobre '
                             'una función que inicialmente no tenía. Al restringir el dominio se puede conseguir que '
                             'la función sea biyectiva y por tanto tenga inversa en esa restricción.')

    def _get_first_step_delimited_inverse_help(self) -> HelpStep:
        function_one = Function(function_id=0, expression='(x)**2', x_values_range=(0, 3), is_main_graphic=False)
        function_one.setup_data(plot_range=(-5, 5))
        function_one.x_values, function_one.y_values = function_one.y_values, function_one.x_values

        text = 'En la función descrita se restringe el dominio a [0, 2] permitiendo así que la función no tenga' \
               ' imágenes repetidas para dos valores cualquiera del conjunto inicial, ahora es una función inyectiva,' \
               ' y por tanto biyectiva, ya era suprayectiva antes.'
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
                        text='El desplazamiento sobre el eje horizontal se produce al sumar o restar una constante '
                             'a la variable x.')

    def _get_first_step_elementary_shift(self) -> HelpStep:
        function = Function(function_id=0, expression='(x + 1)**2', x_values_range=(-4, 4), is_main_graphic=False)
        function.setup_data(plot_range=(-5, 5))
        return HelpStep(order=0, functions=[function],
                        text='Para obtener un desplazamiento horizontal hacia la izquierda hay que sumar una constante'
                             ' a la variable x. En este caso hemos cambiado la función f(x)=x² a f(x)=(x + 1)².',
                        function_color='blue')

    def _get_second_step_elementary_shift(self) -> HelpStep:
        function = Function(function_id=0, expression='(x - 1)**2', x_values_range=(-4, 4), is_main_graphic=False)
        function.setup_data(plot_range=(-5, 5))
        return HelpStep(order=1, functions=[function],
                        text='Para obtener un desplazamiento horizontal hacia la derecha hay que restar una constante'
                             ' a la variable x. En este caso hemos cambiado la función f(x)=x² a f(x)=(x - 1)².',
                        function_color='purple')

    def _get_second_help_data_elementary_shift(self) -> HelpData:
        first_step = self._get_third_step_elementary_shift()
        second_step = self._get_fourth_step_elementary_shift()
        function = Function(function_id=0, expression='(x)**2', x_values_range=(-3, 3), is_main_graphic=True)
        function.setup_data(plot_range=(-5, 5))
        return HelpData(order=1, functions=[function], help_steps=[first_step, second_step],
                        title='Apuntes sobre desplazamientos en funciones',
                        text='El desplazamiento sobre el eje vertical se produce al sumar o restar una constante '
                             'a la función completa.')

    def _get_third_step_elementary_shift(self) -> HelpStep:
        function = Function(function_id=0, expression='(x)**2 + 1', x_values_range=(-3, 3), is_main_graphic=False)
        function.setup_data(plot_range=(-5, 5))
        return HelpStep(order=0, functions=[function],
                        text='Para obtener un desplazamiento vertical hacia arriba hay que sumar una constante'
                             ' a la función completa. En este caso hemos cambiado la función f(x)=x² a f(x)=x² + 1.',
                        function_color='blue')

    def _get_fourth_step_elementary_shift(self) -> HelpStep:
        function = Function(function_id=0, expression='(x)**2 - 1', x_values_range=(-3, 3), is_main_graphic=False)
        function.setup_data(plot_range=(-5, 5))
        return HelpStep(order=1, functions=[function],
                        text='Para obtener un desplazamiento vertical hacia abajo hay que restar una constante'
                             ' a la función completa. En este caso hemos cambiado la función f(x)=x² a f(x)=x² - 1.',
                        function_color='purple')

    def _get_indicate_domain_help(self) -> List[HelpData]:
        first_help_data = self._get_first_help_data_domain()
        return [first_help_data]

    def _get_first_help_data_domain(self) -> HelpData:
        function_one = Function(function_id=0, expression='(x)**2', x_values_range=(0, 2), is_main_graphic=True,
                                domain='[0, 2)')
        function_one.setup_data(plot_range=(-5, 5))
        function_two = Function(function_id=0, expression='x', x_values_range=(3, 5), is_main_graphic=True,
                                domain='(3, +inf)')
        function_two.setup_data(plot_range=(-5, 5))
        help_step_one = self._get_first_help_step_domain()
        help_step_two = self._get_second_help_step_domain()
        return HelpData(order=0, title='Apuntes sobre el dominio de una función',
                        functions=[function_one, function_two], help_steps=[help_step_one, help_step_two],
                        text='El dominio de una función son todos los valores que toma x para la función. '
                             'En este caso el dominio de la función es "[0, 2) U (3, +inf)"')

    def _get_first_help_step_domain(self) -> HelpStep:
        function_one = Function(function_id=0, expression='0', x_values_range=(-5, 5), is_main_graphic=False,
                                domain='(-inf, +inf)', is_invert_function=True)
        function_one.setup_data((-5, 5))

        function_two = Function(function_id=0, expression='1', x_values_range=(-5, 5), is_main_graphic=False,
                                domain='(-inf, +inf)', is_invert_function=True)
        function_two.setup_data((-5, 5))

        function_three = Function(function_id=0, expression='4', x_values_range=(-5, 5), is_main_graphic=False,
                                  domain='(-inf, +inf)', is_invert_function=True)
        function_three.setup_data((-5, 5))

        text = 'Para la función dada, los puntos siguientes sí están definidos en el dominio porque las cotas son. '
        return HelpStep(order=0, functions=[function_one, function_two, function_three], text=text,
                        function_color='blue')

    def _get_second_help_step_domain(self) -> HelpStep:
        function_one = Function(function_id=0, expression='2', x_values_range=(-5, 5), is_main_graphic=False,
                                domain='(-inf, +inf)', is_invert_function=True)
        function_one.setup_data((-5, 5))

        function_two = Function(function_id=0, expression='3', x_values_range=(-5, 5), is_main_graphic=False,
                                domain='(-inf, +inf)', is_invert_function=True)
        function_two.setup_data((-5, 5))

        function_three = Function(function_id=0, expression='2.5', x_values_range=(-5, 5), is_main_graphic=False,
                                  domain='(-inf, +inf)', is_invert_function=True)
        function_three.setup_data((-5, 5))

        text = 'Para la función dada los puntos siguientes no están definidos en el dominio porque las cotas son. '
        return HelpStep(order=0, functions=[function_one, function_two, function_three], text=text,
                        function_color='red')

    def _get_indicate_range_help(self) -> List[HelpData]:
        first_help_data = self._get_first_help_data_range()
        return [first_help_data]

    def _get_first_help_data_range(self) -> HelpData:
        function_one = Function(function_id=0, expression='(x)**2', x_values_range=(0, 2), is_main_graphic=True,
                                domain='[0, 2)')
        function_one.setup_data((-5, 5))
        function_two = Function(function_id=0, expression='x + 0.5', x_values_range=(4, 5), is_main_graphic=True,
                                domain='[4, +inf)')
        function_two.setup_data((-5, 5))
        help_step_one = self._get_first_help_step_range()
        help_step_two = self._get_second_help_step_range()
        return HelpData(order=0, title='Apuntes sobre el rango de una función',
                        functions=[function_one, function_two], help_steps=[help_step_one, help_step_two],
                        text='El rango de una función son todos los valores que toma y para la función. '
                             'En este caso el rango de la función es "[0, 4) U [4.5, +inf)"')

    def _get_first_help_step_range(self) -> HelpStep:
        function_one = Function(function_id=0, expression='0', x_values_range=(-5, 5), is_main_graphic=False,
                                domain='(-inf, +inf)')
        function_one.setup_data((-5, 5))

        function_two = Function(function_id=0, expression='4.5', x_values_range=(-5, 5), is_main_graphic=False,
                                domain='(-inf, +inf)')
        function_two.setup_data((-5, 5))

        function_three = Function(function_id=0, expression='5', x_values_range=(-5, 5), is_main_graphic=False,
                                  domain='(-inf, +inf)')
        function_three.setup_data((-5, 5))

        text = 'Para la función dada, los puntos siguientes sí están definidos en el rango porque las cotas son. '
        return HelpStep(order=0, functions=[function_one, function_two, function_three], text=text,
                        function_color='blue')

    def _get_second_help_step_range(self) -> HelpStep:
        function_one = Function(function_id=0, expression='4', x_values_range=(-5, 5), is_main_graphic=False,
                                domain='(-inf, +inf)')
        function_one.setup_data((-5, 5))

        function_two = Function(function_id=0, expression='4.25', x_values_range=(-5, 5), is_main_graphic=False,
                                domain='(-inf, +inf)')
        function_two.setup_data((-5, 5))

        text = 'Para la función dada los puntos siguientes no están definidos en el rango porque las cotas son. '
        return HelpStep(order=0, functions=[function_one, function_two], text=text,
                        function_color='red')

        ########################################

    def _get_maximum_relative_help(self):
        pass

    def _get_maximum_absolute_help(self):
        pass

    def _get_minimum_relative_help(self):
        pass

    def _get_minimum_absolute_help(self):
        pass

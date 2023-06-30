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
        function_one = Function(function_id=0, expression='(x)**2', x_values_range=(-2, 3), is_main_graphic=True,
                                domain='[-2, +inf)')
        function_one.setup_data(plot_range=(-5, 5))
        help_step_one = self._get_first_help_step_domain()
        help_step_two = self._get_second_help_step_domain()
        return HelpData(order=0, title='Apuntes sobre el dominio de una función',
                        functions=[function_one], help_steps=[help_step_one, help_step_two],
                        text='El dominio de una función corresponde al conjunto de valores de entrada para los que la '
                             'función está definida.')

    def _get_first_help_step_domain(self) -> HelpStep:
        text = 'Para la función dada, se puede observar que el rango de valores del dominio comprende desde la abscisa -2 hasta' \
               ' infinito, porque no vemos punto límite para la función por la derecha, así que nos podemos imaginar ' \
               'que continua infinitamente.'
        return HelpStep(order=0, functions=[], text=text, help_range_orientation='vertical', help_ranges=[(-2, 6)])

    def _get_second_help_step_domain(self) -> HelpStep:
        function_one = Function(function_id=0, expression='3', x_values_range=(-4, -3), is_main_graphic=False,
                                domain='[-4, -3]', is_invert_function=False)
        function_one.setup_data((-5, 5))

        text = 'Para las funciones definidas a trozos, el dominio corresponde al conjunto unión de los dominios de las ' \
               'funciones que la forman. En este caso el dominio es [-4, -3] U [-2, +inf). Resaltar el salto en el dominio, ' \
               'no tienen que ser seguidos los valores que puede tomar el dominio.'
        return HelpStep(order=0, functions=[function_one], text=text, function_color='white',
                        help_range_orientation='vertical', help_ranges=[(-4, -3)])

    def _get_indicate_range_help(self) -> List[HelpData]:
        first_help_data = self._get_first_help_data_range()
        return [first_help_data]

    def _get_first_help_data_range(self) -> HelpData:
        function_one = Function(function_id=0, expression='(x)**2', x_values_range=(-2, 3), is_main_graphic=True,
                                domain='[-2, +inf)')
        function_one.setup_data(plot_range=(-5, 5))
        help_step_one = self._get_first_help_step_range()
        help_step_two = self._get_second_help_step_range()
        return HelpData(order=0, title='Apuntes sobre el recorrido de una función',
                        functions=[function_one], help_steps=[help_step_one, help_step_two],
                        text='El recorrido de una función es el conjunto de valores que puede alcanzar la función, es '
                             'decir, el recorrido es el conjunto formado por todas las imágenes de su dominio.')

    def _get_first_help_step_range(self) -> HelpStep:
        text = 'Para la función dada, se puede observar que el rango de valores del recorrido comprende desde la ordenada 0 hasta' \
               ' infinito, porque no podemos observar límite por arriba para los valores que pueda tomar la función.'
        return HelpStep(order=0, functions=[], text=text, help_range_orientation='horizontal', help_ranges=[(0, 6)])

    def _get_second_help_step_range(self) -> HelpStep:
        function_one = Function(function_id=0, expression='-1', x_values_range=(-4, -3), is_main_graphic=False,
                                domain='[-4, -3]', is_invert_function=False)
        function_one.setup_data((-5, 5))

        text = 'Para las funciones definidas a trozos, el recorrido corresponde al conjunto unión de los recorridos de las ' \
               'funciones que la forman. En este caso el recorrido es [-1, -1] U [-2, +inf).'
        return HelpStep(order=0, functions=[function_one], text=text, function_color='white',
                        help_range_orientation='horizontal', help_ranges=[(-1, -1)])

    def _get_maximum_minimum_help(self) -> List[HelpData]:
        first_help_data = self._get_help_maximum_range()
        second_help_data = self._get_help_minimum_range()
        third_help_data = self._get_help_constant_values()
        return [first_help_data, second_help_data, third_help_data]

    def _get_help_maximum_range(self) -> HelpData:
        function_one = Function(function_id=0, expression='(x)**2 - 1', x_values_range=(0, 2), is_main_graphic=True,
                                domain='[0, 2]')
        function_one.setup_data(plot_range=(-5, 5))
        help_step_one = self._get_first_help_step_maximum()
        help_step_two = self._get_second_help_step_maximum()
        help_step_three = self._get_third_help_step_maximum()
        return HelpData(order=0, title='Apuntes sobre máximos y mínimos de una función',
                        functions=[function_one], help_steps=[help_step_one, help_step_two, help_step_three],
                        text='Los puntos máximos en una función son aquellos puntos para los que dado un entorno, su '
                             'valor en la imagen es mayor o igual que el de todos los puntos de ese entorno definidos '
                             'para la función. Pueden ser '
                             'absolutos, si para toda la función se cumple que son máximos, o relativos, si no se cumple '
                             'en toda la función')

    def _get_first_help_step_maximum(self) -> HelpStep:
        text = 'Para la función dada, se puede observar que el punto (2, 3) es un máximo absoluto, al ser el punto con ' \
               'mayor valor de la función.'
        return HelpStep(order=0, functions=[], text=text)

    def _get_second_help_step_maximum(self) -> HelpStep:
        function_one = Function(function_id=0, expression='(4 * x - 8) - 1', x_values_range=(2, 3), is_main_graphic=False,
                                domain='(2, 3]', is_invert_function=False)
        function_one.setup_data(plot_range=(-5, 5))

        text = 'El estudio de máximos y mínimos para las funciones partidas es idéntico a funciones sin partir. En este ' \
               'caso se observa que la función tiene múltiples máximos absolutos al alcanzar su máximo valor en 3. La definición ' \
               'de máximo absoluto indica que el valor de la imagen del punto tiene que ser mayor o igual, permitiendo múltiples valores.'
        return HelpStep(order=1, functions=[function_one], text=text, function_color='white', point_color='white',
                        points=[Point(3, 3, True)])

    def _get_third_help_step_maximum(self) -> HelpStep:
        function_one = Function(function_id=0, expression='((1/3) * x + 4) - 1', x_values_range=(3, 6), is_main_graphic=False,
                                domain='(3, +inf)', is_invert_function=False)
        function_one.setup_data(plot_range=(-5, 5))

        text = 'Al incluir esta tercera función ambos máximos dejan de ser absolutos, ya no hay valores absolutos porque ' \
               'la función sigue creciendo más de lo que se puede observar en la gráfica. El máximo en (3, 3) ya no ' \
               'cumple la definición de máximo porque los valores a su derecha son mayores que él.'
        return HelpStep(order=2, functions=[function_one], text=text, function_color='white', point_color='white',
                        points=[Point(3, 4, True)])

    def _get_help_minimum_range(self) -> HelpData:
        function_one = Function(function_id=0, expression='-(x)**2 + 5', x_values_range=(0, 2), is_main_graphic=True,
                                domain='(0, 2]')
        function_one.setup_data(plot_range=(-5, 5))
        help_step_one = self._get_first_help_step_minimum()
        help_step_two = self._get_second_help_step_minimum()
        help_step_three = self._get_third_help_step_minimum()
        return HelpData(order=1, title='Apuntes sobre máximos y mínimos de una función',
                        functions=[function_one], help_steps=[help_step_one, help_step_two, help_step_three],
                        text='Los puntos mínimos en una función son aquellos puntos para los que dado un entorno, su '
                             'valor en la imagen es menor o igual que el de todos los puntos de ese entorno definidos '
                             'para la función. Pueden ser '
                             'absolutos, si para toda la función se cumple que son mínimos, o relativos, si no se cumple '
                             'en toda la función')

    def _get_first_help_step_minimum(self) -> HelpStep:
        text = 'Para la función dada, se puede observar que el punto (2, 1) es un mínimo absoluto, al ser el punto con ' \
               'menor valor de la función.'
        return HelpStep(order=0, functions=[], text=text)

    def _get_second_help_step_minimum(self) -> HelpStep:
        function_one = Function(function_id=0, expression='-x', x_values_range=(-3, -1), is_main_graphic=False,
                                domain='(-3, -1]', is_invert_function=False)
        function_one.setup_data(plot_range=(-5, 5))

        text = 'En este caso se observa que la función tiene múltiples mínims absolutos al alcanzar su mínimo valor en 1.' \
               ' La definición de mínimo absoluto indica que el valor de la imagen del punto tiene que ser menor o igual,' \
               ' permitiendo múltiples valores.'
        return HelpStep(order=1, functions=[function_one], text=text, function_color='white', point_color='white',
                        points=[Point(-1, 1, True)])

    def _get_third_help_step_minimum(self) -> HelpStep:
        function_one = Function(function_id=0, expression='-2', x_values_range=(-1, 0), is_main_graphic=False,
                                domain='(-1, 0)', is_invert_function=False)
        function_one.setup_data(plot_range=(-5, 5))

        text = 'Al incluir esta tercera función ambos mínimos dejan de ser absolutos, ya no hay valores absolutos porque ' \
               'no se cumple que la imagen de esos valores es la menor o igual que el resto de imágenes. El mínimo en (-1, 1) ya no ' \
               'cumple la definición de mínimo porque los valores a su derecha son menores que él.'
        return HelpStep(order=2, functions=[function_one], text=text, function_color='white')

    def _get_help_constant_values(self) -> HelpData:
        function_one = Function(function_id=0, expression='2', x_values_range=(-2, 2), is_main_graphic=True,
                                domain='(-2, 2]')
        function_one.setup_data(plot_range=(-5, 5))

        help_step_one = self._get_first_help_constant_minimum()
        help_step_two = self._get_second_help_step_minimum()
        return HelpData(order=2, title='Apuntes sobre máximos y mínimos de una función',
                        functions=[function_one], help_steps=[help_step_one, help_step_two],
                        text='Las funciones constantes son funciones que cumplen que todos los puntos en su dominio '
                             'son máximos y mínimos absolutos.')

    def _get_first_help_constant_minimum(self) -> HelpStep:
        text = 'Para la función dada todos los valores de la función constante y=-2 son los mayores y menores posibles,' \
               ' por lo que todos ellos son máximos y mínimos absolutos.'
        return HelpStep(order=0, functions=[], text=text)

    def _get_second_help_constant_minimum(self) -> HelpStep:
        function_one = Function(function_id=0, expression='2 * (x) + 6', x_values_range=(-3, -2), is_main_graphic=False,
                                domain='(-3, -2)', is_invert_function=False)
        function_one.setup_data(plot_range=(-5, 5))

        text = 'En este caso, al introducir una nueva función todos los puntos de la función constante dejan de ser mínimos ' \
               'absolutos para ser mínimos relativos, excepto el punto (-2, 2) que no es mínimo relativo porque tiene valores' \
               ' por la izquierda menores a él.'
        return HelpStep(order=1, functions=[function_one], text=text, function_color='white')
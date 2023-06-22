from ..elementary_graph_components import ElementaryGraphComponent
from ...factories import PlotFactory2
from ...models import ExerciseResume, FunctionExercise, FunctionStep, Point


class InverseConceptComponent(ElementaryGraphComponent):
    label = 'Indicar si existe inversa: '

    def __init__(self, exercise: FunctionExercise, step: FunctionStep, resume: ExerciseResume, need_help_data: bool):
        super(InverseConceptComponent, self).__init__(
            exercise=exercise, step=step, resume=resume, need_help_data=need_help_data, show_main_function_limits=False,
            show_function_labels=False
        )

    def _setup_data(self):
        main_function = self._exercise.get_main_function()
        main_function.setup_data(plot_range=self._exercise.plot_range)

    def _get_options_to_display(self):
        return ['SÍ', 'NO']

    def _get_function_to_draw(self):
        return self._exercise.get_main_function()

    def _get_correct_expression(self):
        return 'SÍ' if self._exercise.has_main_function_inverse() else 'NO'

    def _setup_correct_response(self):
        self._result_label.setText(f'Correcto.')
        self._result_label.setStyleSheet('color: green;')
        self._result_label.setVisible(True)

        pressed_button = self._graph_buttons[self._button_selected_index]
        pressed_button.setStyleSheet("""
            #primary {
                background-color: #F5EBE0;
                border: 1px solid #A57A51; 
                border-radius: 10px;
                padding: 3px;
                font-size: 20px;
                color: green;
            }

            #primary:hover {
                border: 3px solid #A57A51; 
            }
            """
                                     )

    def _setup_wrong_response(self, expression_selected: str):
        if expression_selected == 'SÍ':
            self._setup_wrong_yes_inverse_response()
        elif expression_selected == 'NO':
            self._result_label.setText(f'Incorrecto. No hay imágenes repetidas en la función.')

        self._result_label.setStyleSheet('color: red;')
        self._result_label.setVisible(True)

        pressed_button = self._graph_buttons[self._button_selected_index]
        pressed_button.setStyleSheet("""
            #primary {
                background-color: #F5EBE0;
                border: 1px solid #A57A51; 
                border-radius: 10px;
                padding: 3px;
                font-size: 20px;
                color: red;
            }

            #primary:hover {
                border: 3px solid #A57A51; 
            }
            """
                                     )

        correct_button = next(
            button for button in self._graph_buttons if button.text() == self._get_correct_expression()
        )
        correct_button.setStyleSheet("""
            #primary {
                background-color: #F5EBE0;
                border: 1px solid #A57A51; 
                border-radius: 10px;
                padding: 3px;
                font-size: 20px;
                color: green;
            }

            #primary:hover {
                border: 3px solid #A57A51; 
            }
            """
                                     )

    def _setup_wrong_yes_inverse_response(self):
        self._result_label.setText(f'Incorrecto. Hay imágenes repetidas en la función.')
        main_function = self._get_function_to_draw()
        values = [
            (x, y) for x_group, y_group in zip(main_function.x_values, main_function.y_values)
            for x, y in zip(x_group, y_group)
            if self._exercise.plot_range[0] + 0.5 < x < self._exercise.plot_range[1] - 0.5 and
               self._exercise.plot_range[0] + 0.5 < y < self._exercise.plot_range[1] - 0.5
        ]

        y_values_set = set()
        x_by_y = {}
        points = []

        for x, y in values:
            if y not in y_values_set:
                y_values_set.add(y)
                x_by_y[y] = x
            else:
                points = [Point(x, y), Point(x_by_y[y], y)]
        PlotFactory2.set_points(self._plot_widget, points=points, color='red')

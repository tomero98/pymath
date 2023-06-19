from ..elementary_graph_components import ElementaryGraphComponent
from ...models import ExerciseResume, FunctionExercise, FunctionStep


class InverseConceptComponent(ElementaryGraphComponent):
    label = 'Indicar si existe inversa: '

    def __init__(self, exercise: FunctionExercise, step: FunctionStep, resume: ExerciseResume, need_help_data: bool):
        super(InverseConceptComponent, self).__init__(
            exercise=exercise, step=step, resume=resume, need_help_data=need_help_data, show_main_function_limits=False,
            show_function_labels=False
        )

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
        self._result_label.setText(f'Incorrecto. La expresión esperada es {self._get_correct_expression()}')
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

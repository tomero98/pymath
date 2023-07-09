from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QWidget

from src.projectConf.factories import ButtonFactory
from ..graph_interaction_validation_component import GraphInteractionValidationComponent
from ...factories import PlotFactory2
from ...models import ExerciseResume, FunctionExercise, FunctionStep, Function


class ElementaryGraphComponent(GraphInteractionValidationComponent):
    label = 'Seleccionar la función elemental.'

    def __init__(self, exercise: FunctionExercise, step: FunctionStep, resume: ExerciseResume, need_help_data: bool,
                 show_function_labels: bool = True, show_main_function_limits: bool = False):
        super(ElementaryGraphComponent, self).__init__(
            exercise=exercise, step=step, resume=resume, need_help_data=need_help_data,
            show_function_labels=show_function_labels, show_main_function_limits=show_main_function_limits
        )

        self._button_selected_index: int = None  # noqa

        self._graph_buttons: List[QPushButton] = []  # noqa
        self._bottom_buttons_layout: QHBoxLayout = None  # noqa
        self._bottom_buttons_widget: QWidget = None  # noqa

    def _setup_layout(self):
        self._layout.addWidget(self._question_label, alignment=Qt.AlignHCenter)
        self._layout.addWidget(self._plot_widget_container, alignment=Qt.AlignHCenter)
        self._layout.addSpacing(20)
        self._layout.addWidget(self._bottom_buttons_widget, alignment=Qt.AlignHCenter)
        self._layout.addWidget(self._result_label, alignment=Qt.AlignHCenter)

    def _is_exercise_correct(self, expression_selected) -> bool:
        correct_expression = self._get_correct_expression()
        return expression_selected == correct_expression

    def _on_click_validation_button(self):
        pass

    def _on_function_to_draw_click(self, plot_curve_item_selected, point_selected):
        pass

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


        PlotFactory2.set_functions(graph=self._plot_widget, functions=[self._get_function_to_draw()], function_width=3,
                                   color='green')
        label_functions = [(self._get_function_to_draw(), 'green')]
        PlotFactory2.set_labels(graph=self._plot_widget, functions=label_functions)

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

        error_function = self._get_error_function(expression=expression_selected)
        error_function.setup_data(plot_range=(-5, 5))
        PlotFactory2.set_functions(graph=self._plot_widget, functions=[self._get_function_to_draw()], function_width=3,
                                   color='green')
        PlotFactory2.set_functions(graph=self._plot_widget, functions=[error_function], function_width=3,
                                   color='red')
        label_functions = [(self._get_function_to_draw(), 'green'), (error_function, 'red')]
        PlotFactory2.set_labels(graph=self._plot_widget, functions=label_functions)

    def _setup_finished_exercise(self):
        super(ElementaryGraphComponent, self)._setup_finished_exercise()
        for button in self._graph_buttons:
            button.setDisabled(True)

    def _setup_components(self):
        super(ElementaryGraphComponent, self)._setup_components()
        self._bottom_buttons_widget = self._get_function_expression_buttons_widget()
        self._result_label.setText('')
        self._result_label.setVisible(True)

    def _get_function_to_draw(self):
        return self._exercise.get_main_function()[0]

    def _apply_resume(self):
        self._button_selected_index = next(
            index for index, button in enumerate(self._graph_buttons) if button.text() == self._resume.response
        )
        super(ElementaryGraphComponent, self)._apply_resume()

    def _get_function_expression_buttons_widget(self) -> QWidget:
        window = QWidget()
        window.setObjectName('container')

        layout = QHBoxLayout()
        layout.addStretch()
        options = self._get_options_to_display()
        for index, option in enumerate(options):
            graph_button = self._get_graph_button(index=index, option=option)
            layout.addWidget(graph_button)
            graph_button.adjustSize()
            self._graph_buttons.append(graph_button)
            layout.addStretch()
        window.setLayout(layout)
        window.setMinimumSize(QSize(window.minimumSizeHint().width() * 2, window.minimumSizeHint().height() * 1.3))
        window.setMaximumSize(QSize(window.minimumSizeHint().width() * 2, window.minimumSizeHint().height() * 1.3))
        return window

    def _get_graph_button(self, index: int, option: str) -> QPushButton:
        return ButtonFactory.get_button_component(
            title=option, minimum_width=120, minimum_height=45, text_size=40, primary_button=True,
            function_to_connect=lambda val=index: self._execute_validation(button_index=index),
        )

    def _execute_validation(self, button_index: int):
        self._button_selected_index = button_index
        pressed_button = self._graph_buttons[button_index]
        self._validate_exercise(expression_selected=pressed_button.text())

    def _get_options_to_display(self):
        return [function.get_math_expression() for function in self._exercise.functions]

    def _get_correct_expression(self):
        return self._exercise.get_main_function()[0].get_math_expression()

    def _get_error_function(self, expression: str) -> Function:
        return next(function for function in self._exercise.functions if function.get_math_expression() == expression)

    def _validate_exercise(self, expression_selected, is_resume: bool = False):
        super(ElementaryGraphComponent, self)._validate_exercise(expression_selected=expression_selected,
                                                                 is_resume=is_resume)
        is_answer_correct = self._is_exercise_correct(expression_selected=expression_selected)
        if is_answer_correct:
            self._setup_correct_response()
        else:
            self._setup_wrong_response(expression_selected=expression_selected)
        self._setup_finished_exercise()

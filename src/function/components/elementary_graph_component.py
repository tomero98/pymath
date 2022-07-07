from typing import List

import pyqtgraph
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout

from ..factories import PlotFactory
from ..models.function import Function
from ..models.function_exercise import FunctionExercise
from ..models.function_step import FunctionStep
from ...projectConf.factories import LabelFactory, ButtonFactory
from ...projectConf.factories.icon_factory import IconFactory
from ...projectConf.models.enums.text_type import TextType


class ElementaryGraphComponent(QWidget):
    continue_signal = pyqtSignal(bool)

    def __init__(self, exercise: FunctionExercise, step: FunctionStep):
        super(ElementaryGraphComponent, self).__init__()
        self._exercise = exercise
        self._step = step

        self._plot_widget: pyqtgraph.PlotWidget = None  # noqa
        self._help_subtitle_widget: QLabel = None  # noqa
        self._graph_buttons: List[QPushButton] = []  # noqa
        self._help_text: QLabel = None  # noqa

        self._layout: QVBoxLayout = None  # noqa
        self._main_window_layout: QHBoxLayout = None  # noqa
        self._bottom_buttons_layout: QHBoxLayout = None  # noqa

        self._draw()

    def _draw(self):
        self._layout = QVBoxLayout()
        question_widget = LabelFactory.get_label_component(text=self._step.question, label_type=TextType.SUBTITLE)
        self._main_window_layout = self._get_main_window_layout(self._exercise)
        self._bottom_buttons_layout = self._get_bottom_buttons_layout()
        self._help_text = LabelFactory.get_label_component(text='', label_type=TextType.NORMAL_TEXT,
                                                           need_word_wrap=True)

        icon = IconFactory.get_icon_widget(image_name='continue_button.png')
        self._continue_button = ButtonFactory.get_button_component(
            title='', function_to_connect=lambda: self._send_continue_signal(), icon=icon, icon_size=40,
            tooltip='Continuar', is_disable=True)

        self._layout.addWidget(question_widget, alignment=Qt.AlignHCenter)
        self._layout.addLayout(self._main_window_layout)
        self._layout.addSpacing(15)
        self._layout.addLayout(self._bottom_buttons_layout)
        self._layout.addWidget(self._help_text, alignment=Qt.AlignHCenter)
        self._layout.addWidget(self._continue_button, alignment=Qt.AlignLeft)
        self.setLayout(self._layout)

    def _get_main_window_layout(self, exercise: FunctionExercise) -> QHBoxLayout:
        main_window_layout = QHBoxLayout()
        self._plot_widget = PlotFactory.get_plot([exercise.get_main_function()], show_ends=False)

        main_window_layout.addStretch()
        main_window_layout.addWidget(self._plot_widget, alignment=Qt.AlignHCenter)
        main_window_layout.addStretch()
        return main_window_layout

    def _get_bottom_buttons_layout(self) -> QHBoxLayout:
        layout = QHBoxLayout()

        for index, graph in enumerate(self._exercise.functions):
            graph_button = self._get_graph_button(index=index, graph=graph)
            layout.addWidget(graph_button)
            self._graph_buttons.append(graph_button)
        return layout

    def _get_graph_button(self, index: int, graph: Function) -> QPushButton:
        return ButtonFactory.get_button_component(
            title=graph.get_math_expression(), minimum_width=25,
            function_to_connect=lambda val=index: self._validate_exercise(button_index=index)
        )

    def _validate_exercise(self, button_index):
        pressed_button = self._graph_buttons[button_index]
        correct_expression = self._exercise.get_main_function().get_math_expression()
        is_answer_correct = pressed_button.text() == correct_expression
        border_color = '#2F8C53' if is_answer_correct else 'red'
        if not is_answer_correct:
            self._help_text.setText('Incorrecto.')
            correct_button = next(button for button in self._graph_buttons if button.text() == correct_expression)
            correct_button.setStyleSheet('background: #2F8C53')
        else:
            self._help_text.setText('Correcto.')
        self._help_text.setStyleSheet(f'color: {border_color}')
        pressed_button.setStyleSheet(f'background: {border_color}')
        self._continue_button.setStyleSheet(f'background: {border_color}')
        self._continue_button.setDisabled(False)
        for button in self._graph_buttons:
            button.setDisabled(True)

    def _send_continue_signal(self):
        self.continue_signal.emit(True)

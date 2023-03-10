from typing import List

import pyqtgraph
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton

from src.function.factories.plot_factory2 import PlotFactory2
from src.function.models import HelpData, HelpStep
from src.projectConf.factories import IconFactory, ButtonFactory, LabelFactory
from src.projectConf.models.enums import TextType


class HelpDataDialog(QWidget):
    def __init__(self, help_data_list: List[HelpData], show_main_function_limits: bool = False,
                 show_function_labels: bool = False):
        super(HelpDataDialog, self).__init__()
        self._help_data_list = help_data_list
        self._show_main_function_limits = show_main_function_limits
        self._show_function_labels = show_function_labels

        self._plot_widget: pyqtgraph.PlotWidget = None  # noqa
        self._continue_button: QPushButton = None  # noqa
        self._back_button: QPushButton = None  # noqa
        self._text_label: QLabel = None  # noqa
        self._current_help_data: HelpData = None  # noqa
        self._current_step: HelpStep = None  # noqa

    def draw(self):
        self.setWindowTitle('Ayuda')

        help_layout = QVBoxLayout()

        self._plot_widget = PlotFactory2.get_plot(function_range=self._help_data_list[0].function.domain)
        PlotFactory2.set_functions(graph=self._plot_widget, functions=[self._help_data_list[0].function],
                                   function_width=5, color='white', show_limits=self._show_main_function_limits)
        if self._show_function_labels:
            PlotFactory2.set_labels(graph=self._plot_widget, functions=[(self._help_data_list[0].function, 'white')])
        help_layout.addWidget(self._plot_widget)

        self._text_label = LabelFactory.get_label_component(
            text=self._help_data_list[0].text, label_type=TextType.SUBTITLE, align=Qt.AlignHCenter, need_word_wrap=True,
            set_visible=True
        )
        help_layout.addWidget(self._text_label)

        buttons_layout = self._get_buttons_layout()
        help_layout.addLayout(buttons_layout)

        self.setLayout(help_layout)
        self.show()
        self.setFixedSize(self.width(), self.height())

        self._current_help_data = self._help_data_list[0]
        self._current_step = None

    def _get_buttons_layout(self):
        buttons_layout = QHBoxLayout()

        icon = IconFactory.get_icon_widget(image_name='continue_button.png')
        continue_button_is_active = (len(self._help_data_list) > 1) or (len(self._help_data_list[0].help_steps) > 1)
        self._continue_button = ButtonFactory.get_button_component(
            title='', function_to_connect=lambda: self._execute_continue(), icon=icon, icon_size=85,
            tooltip='Continuar', is_disable=not continue_button_is_active
        )

        icon = IconFactory.get_icon_widget(image_name='back_2_button.png')
        self._back_button = ButtonFactory.get_button_component(
            title='', function_to_connect=lambda: self._execute_back(), icon=icon, icon_size=85,
            tooltip='Ir al ejercicio anterior', is_disable=True
        )

        buttons_layout.addStretch()
        buttons_layout.addWidget(self._back_button)
        buttons_layout.addStretch()
        buttons_layout.addStretch()
        buttons_layout.addWidget(self._continue_button)
        buttons_layout.addStretch()
        return buttons_layout

    def _execute_back(self):
        if not self._current_step:
            index = self._current_help_data.order - 1
            self._current_help_data = self._help_data_list[index]
            self._current_step = self._current_help_data.help_steps[-1]
        elif self._current_step.order == 0:
            self._current_step = None
        else:
            index = self._current_step.order - 1
            self._current_step = self._current_help_data.help_steps[index]

        PlotFactory2.reset_graph(graph=self._plot_widget)

        text = self._current_step.text if self._current_step else self._current_help_data.text
        self._text_label.setText(text)
        PlotFactory2.set_functions(graph=self._plot_widget, functions=[self._current_help_data.function],
                                   function_width=5, color='white', show_limits=self._show_main_function_limits)
        if self._show_function_labels:
            PlotFactory2.set_labels(graph=self._plot_widget, functions=[(self._current_help_data.function, 'white')])
        if self._current_step:
            steps = [step for step in self._current_help_data.help_steps if step.order <= self._current_step.order]
            for step in steps:
                PlotFactory2.set_functions(graph=self._plot_widget, functions=step.functions, color=step.function_color)
                if self._show_function_labels:
                    functions = [(function, step.function_color) for function in step.functions]
                    PlotFactory2.set_labels(graph=self._plot_widget, functions=functions)

                PlotFactory2.set_points(graph=self._plot_widget, points=step.points,
                                        color=step.point_color)

        self._setup_buttons_state()

    def _execute_continue(self):
        index = self._current_step.order + 1 if self._current_step else 0
        try:
            self._current_step = self._current_help_data.help_steps[index]
            self._setup_step()
        except IndexError:
            index = self._current_help_data.order + 1
            self._current_step = None
            self._current_help_data = self._help_data_list[index]
            self._setup_help_data()
        self._setup_buttons_state()

    def _setup_step(self):
        PlotFactory2.set_functions(graph=self._plot_widget, functions=self._current_step.functions,
                                   color=self._current_step.function_color)
        if self._show_function_labels:
            functions = [(function, self._current_step.function_color) for function in self._current_step.functions]
            PlotFactory2.set_labels(graph=self._plot_widget, functions=functions)

        PlotFactory2.set_points(graph=self._plot_widget, points=self._current_step.points,
                                color=self._current_step.point_color)

        self._text_label.setText(self._current_step.text)

    def _setup_help_data(self):
        PlotFactory2.reset_graph(graph=self._plot_widget)
        PlotFactory2.set_functions(graph=self._plot_widget, functions=[self._current_help_data.function],
                                   function_width=5, color='white', show_limits=self._show_main_function_limits)
        if self._show_function_labels:
            PlotFactory2.set_labels(graph=self._plot_widget, functions=[(self._current_help_data.function, 'white')])

        self._text_label.setText(self._current_help_data.text)

    def _setup_buttons_state(self):
        is_first_step = self._current_help_data.order == 0 and self._current_step is None
        is_last_help_data = (self._current_help_data.order + 1) == len(self._help_data_list)
        if len(self._help_data_list[-1].help_steps) and self._current_step:
            is_last_step = len(self._help_data_list[-1].help_steps) == 0 \
                           or len(self._help_data_list[-1].help_steps) == (self._current_step.order + 1)
        else:
            is_last_step = False
        is_last_step = is_last_help_data and is_last_step
        self._continue_button.setDisabled(is_last_step)
        self._back_button.setDisabled(is_first_step)

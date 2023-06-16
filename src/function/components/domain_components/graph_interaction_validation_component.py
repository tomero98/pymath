from abc import abstractmethod

import pyqtgraph
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy

from src.projectConf.factories import LabelFactory, ButtonFactory, IconFactory
from src.projectConf.models.enums import TextType
from ..component import Component
from ...factories import PlotFactory2
from ...models import ExerciseResume, FunctionExercise, FunctionStep
from ...models.enums import ResumeState


class GraphInteractionValidationComponent(Component):
    def __init__(self, exercise: FunctionExercise, step: FunctionStep, resume: ExerciseResume,
                 need_help_data: bool = False, show_main_function_limits: bool = False,
                 show_function_labels: bool = False):
        super(GraphInteractionValidationComponent, self).__init__(
            exercise=exercise, step=step, resume=resume, need_help_data=need_help_data,
            show_main_function_limits=show_main_function_limits, show_function_labels=show_function_labels
        )

        self._layout: QVBoxLayout = None  # noqa
        self._question_label: QLabel = None  # noqa
        self._validate_button: QPushButton = None  # noqa
        self._plot_widget: pyqtgraph.PlotWidget = None  # noqa
        self._plot_widget_layout: QHBoxLayout = None  # noqa
        self._info_button_layout: QVBoxLayout = None  # noqa
        self._button_layout: QVBoxLayout = None  # noqa

    @abstractmethod
    def _get_correct_expression(self):
        pass

    def _setup_data(self):
        pass

    def _draw(self):
        self._layout = QVBoxLayout()
        self._setup_components()
        self._setup_layout()
        self.setLayout(self._layout)

    def _setup_components(self):
        super(GraphInteractionValidationComponent, self)._setup_components()
        self._question_label = self._get_question_label()
        self._validate_button = self._get_validate_button()
        self._plot_widget_layout = self._get_plot_widget_layout()

    def _setup_layout(self):
        pass

    def _get_question_label(self) -> QLabel:
        return LabelFactory.get_label_component(text=self._step.question, label_type=TextType.SUBTITLE,
                                                align=Qt.AlignHCenter)

    def _get_validate_button(self) -> QPushButton:
        icon = IconFactory.get_icon_widget(image_name='check_exercise.png')
        return ButtonFactory.get_button_component(
            title='', function_to_connect=self._on_click_validation_button, primary_button=True, icon=icon,
            icon_size=45, tooltip='Comprobar ejercicio'
        )

    @abstractmethod
    def _on_click_validation_button(self):
        pass

    def _get_plot_widget_layout(self) -> QHBoxLayout:
        layout = QHBoxLayout()

        self._plot_widget = self._get_plot_widget()
        self._button_layout = self._get_button_layout()

        layout.addStretch()
        layout.addWidget(self._plot_widget, alignment=Qt.AlignTop | Qt.AlignHCenter)
        layout.addLayout(self._button_layout)
        return layout

    def _get_plot_widget(self) -> pyqtgraph.PlotWidget:
        plot_widget = PlotFactory2.get_plot(function_range=self._exercise.plot_range)
        PlotFactory2.set_functions(graph=plot_widget, functions=[self._exercise.get_main_function()],
                                   function_width=5, color='white', show_limits=self._show_main_function_limits)
        return plot_widget

    def _get_button_layout(self) -> QVBoxLayout:
        layout = QVBoxLayout()

        self._info_button_layout = self._get_info_button_layout()

        layout.addLayout(self._info_button_layout)
        return layout

    def _get_info_button_layout(self) -> QHBoxLayout:
        layout = QHBoxLayout()

        layout.addWidget(self._info_button, alignment=Qt.AlignTop)
        layout.addWidget(self._help_button, alignment=Qt.AlignTop)
        layout.addStretch()

        return layout

    @abstractmethod
    def _on_function_to_draw_click(self, plot_curve_item_selected, point_selected):
        pass

    def _apply_resume(self):
        expression_selected = self._resume.response
        self._validate_exercise(expression_selected=expression_selected, is_resume=True)

    def _validate_exercise(self, expression_selected, is_resume: bool = False):
        is_answer_correct = self._is_exercise_correct(expression_selected=expression_selected)

        if not is_resume:
            self._update_resume(expression_selected=expression_selected, is_answer_correct=is_answer_correct)

        self.resume_signal.emit(self._resume)

    @abstractmethod
    def _is_exercise_correct(self, expression_selected):
        pass

    def _update_resume(self, expression_selected: str, is_answer_correct: bool):
        resume_state = ResumeState.success if is_answer_correct else ResumeState.error
        self._resume.resume_state = resume_state
        self._resume.response = expression_selected

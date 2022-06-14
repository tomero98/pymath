import pyqtgraph
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QApplication

from ..factories import PlotFactory
from ..models.function_exercise import FunctionExercise
from ..models.function_step import FunctionStep
from ...projectConf.factories import LabelFactory, ButtonFactory
from ...projectConf.models.enums.text_type import TextType


class InverseSelectionComponent(QWidget):
    continue_signal = pyqtSignal(bool)

    def __init__(self, exercise: FunctionExercise, step: FunctionStep):
        super(InverseSelectionComponent, self).__init__()
        self._exercise = exercise
        self._step = step
        self._is_answer_correct = True
        self._exercise_result = None
        self._inverse_points = self._exercise.get_inverse_graph().get_points_grouped()
        self._all_points_not_duplicated = self._exercise.get_all_points_not_duplicated(include_main_graphic=False,
                                                                                       include_inverse_points=True)

        self._plot_widget: pyqtgraph.PlotWidget = None
        self._help_subtitle_widget: QLabel = None
        self._ok_button: QPushButton = None
        self._fail_button: QPushButton = None
        self._help_text: QLabel = None

        self._layout: QVBoxLayout = None
        self._main_window_layout: QHBoxLayout = None
        self._bottom_buttons_layout: QHBoxLayout = None

        self._draw()

    def _draw(self):
        self._layout = QVBoxLayout()
        question_widget = LabelFactory.get_label_component(text=self._step.question, label_type=TextType.SUBTITLE)
        self._main_window_layout = self._get_main_window_layout()
        self._help_text = LabelFactory.get_label_component(text='', label_type=TextType.NORMAL_TEXT)
        self._continue_button = ButtonFactory.get_button_component(
            title='Continuar', function_to_connect=lambda: self._send_continue_signal(), is_disable=True
        )
        self._layout.addWidget(question_widget)
        self._layout.addLayout(self._main_window_layout)
        self._layout.addWidget(self._help_text)
        self._layout.addWidget(self._continue_button, alignment=Qt.AlignRight)
        self.setLayout(self._layout)

    def _get_main_window_layout(self) -> QHBoxLayout:
        main_window_layout = QHBoxLayout()

        inverse_function = self._exercise.get_inverse_graph()
        self._plot_widget = PlotFactory.get_plot([*self._exercise.functions, inverse_function])

        main_window_layout.addStretch()
        main_window_layout.addWidget(self._plot_widget)
        main_window_layout.addStretch()
        self.proxy = pyqtgraph.SignalProxy(self._plot_widget.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved)
        self.proxy2 = pyqtgraph.SignalProxy(self._plot_widget.scene().sigMouseClicked, rateLimit=60, slot=self.onClick)
        return main_window_layout

    def mouseMoved(self, e):
        pos = e[0]
        if self._plot_widget.sceneBoundingRect().contains(pos):
            mousePoint = self._plot_widget.getPlotItem().vb.mapSceneToView(pos)
            x_position = round(mousePoint.x(), 1)
            y_position = round(mousePoint.y(), 1)

            if (x_position, y_position) in self._all_points_not_duplicated:
                QApplication.setOverrideCursor(Qt.PointingHandCursor)
            else:
                QApplication.restoreOverrideCursor()

    def onClick(self, e):
        pos = e[0].pos()
        if self._plot_widget.sceneBoundingRect().contains(pos) and self._exercise_result is None:
            mousePoint = self._plot_widget.getPlotItem().vb.mapSceneToView(pos)
            # Added 0.8 deviation to supply diffs between mouse moved and mouse click
            x_position = round(mousePoint.x(), 1) + 0.8
            y_position = round(mousePoint.y(), 1)

            if (x_position, y_position) in self._all_points_not_duplicated:
                self._validate_exercise(response_coor=(x_position, y_position))

    def setup_help_data(self):
        self._set_help_text()
        self._update_plot_with_help_data()

    def _set_help_text(self):
        self._help_text.setText(self._step.function_help_data.help_text)
        self._help_text.setStyleSheet(f'color: blue')

    def _update_plot_with_help_data(self):
        inverse_function = self._exercise.get_inverse_graph()
        current_functions = [*self._exercise.functions, inverse_function]
        functions_to_update = self._step.function_help_data.help_expressions
        PlotFactory.update_plot(plot_widget=self._plot_widget, current_functions=current_functions,
                                functions_to_update=functions_to_update, is_help_data=True)

    def _validate_exercise(self, response_coor: tuple):
        self._is_answer_correct = response_coor in self._inverse_points
        border_color = 'green' if self._is_answer_correct else 'red'
        self._continue_button.setStyleSheet(f'border: 3px solid {border_color}')
        self._plot_widget.setStyleSheet(f'border: 3px solid {border_color}')
        self._continue_button.setDisabled(False)
        if not self._is_answer_correct:
            self._update_plot_with_error_data()

    def _update_plot_with_error_data(self):
        self._help_text.setText(f'Recuerda que: "{self._step.function_help_data.help_text}". Por lo que en este caso '
                                f'habría que delimitar el dominio de la función.')
        self._help_text.setStyleSheet(f'color: red')
        inverse_function = self._exercise.get_inverse_graph()
        current_functions = [*self._exercise.functions, inverse_function]
        functions_to_update = self._step.function_help_data.help_expressions
        PlotFactory.update_plot(plot_widget=self._plot_widget, current_functions=current_functions,
                                functions_to_update=functions_to_update)

    def _send_continue_signal(self):
        self.continue_signal.emit(self._is_answer_correct)

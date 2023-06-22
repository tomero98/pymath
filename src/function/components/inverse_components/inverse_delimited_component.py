import pyqtgraph
from PyQt5.QtCore import pyqtSignal, Qt, QSize
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget

from ..domain_components.domain_definition_component import DomainDefinitionComponent
from ...factories import PlotFactory2
from ...models import FunctionExercise, FunctionStep, ExerciseResume, Point


class InverseDelimitedComponent(DomainDefinitionComponent):
    continue_signal = pyqtSignal(bool)
    label = 'Seleccionar la inversa'

    def __init__(self, exercise: FunctionExercise, step: FunctionStep, resume: ExerciseResume,
                 need_help_data: bool = False):
        super(InverseDelimitedComponent, self).__init__(
            exercise=exercise, step=step, resume=resume, need_help_data=need_help_data, show_function_labels=False,
            show_main_function_limits=False
        )

        self._region: pyqtgraph.LinearRegionItem = None  # noqa

    def _setup_data(self):
        main_function = self._exercise.get_main_function()
        main_function.setup_data(plot_range=self._exercise.plot_range)

    def _get_function_to_draw(self):
        return self._exercise.get_main_function()

    def _setup_layout(self):
        super(InverseDelimitedComponent, self)._setup_layout()
        self._validate_button.setDisabled(False)

    def _get_button_layout(self) -> QVBoxLayout:
        layout = QVBoxLayout()

        self._info_button_layout = self._get_info_button_layout()

        layout.addLayout(self._info_button_layout)
        return layout

    def _is_exercise_correct(self, expression_selected: tuple):
        main_function = self._exercise.get_main_function()
        y_values_selected = [
            y for x_group, y_group in zip(main_function.x_values, main_function.y_values)
            for x, y in zip(x_group, y_group) if expression_selected[0] <= x <= expression_selected[1]
        ]
        return len(set(y_values_selected)) == len(y_values_selected)

    def _get_plot_widget(self) -> pyqtgraph.PlotWidget:
        plot_widget = PlotFactory2.get_plot(function_range=self._exercise.plot_range)
        PlotFactory2.set_functions(graph=plot_widget, functions=[self._exercise.get_main_function()],
                                   function_width=5, color='white', show_limits=self._show_main_function_limits)
        self._region = pyqtgraph.LinearRegionItem(values=(-1, 1), orientation='vertical', swapMode='sort',
                                                  bounds=self._exercise.plot_range)
        plot_widget.addItem(self._region)
        return plot_widget

    def _get_domain_expression_edit_widget(self) -> QWidget:
        widget = QWidget()
        widget.setObjectName('topic-container')

        layout = QHBoxLayout()
        layout.addWidget(self._validate_button, alignment=Qt.AlignTop | Qt.AlignHCenter)

        widget.setLayout(layout)
        widget.setMinimumSize(QSize(widget.minimumSizeHint().width() * 1.4, widget.minimumSizeHint().height() * 1.2))
        return widget

    def _on_click_validation_button(self):
        response = self._region.getRegion()
        expression_selected = f'{response[0]}, {response[1]}'
        self._validate_exercise(expression_selected=expression_selected)

    def _validate_exercise(self, expression_selected: str, is_resume: bool = False):
        expression_selected_str = expression_selected
        expression_selected = tuple(map(float, expression_selected.split(',')))
        is_answer_correct = self._is_exercise_correct(expression_selected=expression_selected)
        if not is_resume:
            self._update_resume(expression_selected=expression_selected_str, is_answer_correct=is_answer_correct)

        self.resume_signal.emit(self._resume)

        if is_resume:
            self._region.setRegion(expression_selected)

        if is_answer_correct:
            self._setup_correct_response()
        else:
            self._setup_wrong_response(expression_selected=expression_selected_str)
        self._setup_finished_exercise()

    def _setup_wrong_response(self, expression_selected: str):
        main_function = self._exercise.get_main_function()
        expression_selected = tuple(map(float, expression_selected.split(',')))
        values_selected = [
            (x, y) for x_group, y_group in zip(main_function.x_values, main_function.y_values)
            for x, y in zip(x_group, y_group) if expression_selected[0] <= x <= expression_selected[1]
        ]
        y_values_set = set()
        x_by_y = {}
        points = None
        for x, y in values_selected:
            if y not in y_values_set:
                y_values_set.add(y)
                x_by_y[y] = x
            else:
                points = [Point(x, y), Point(x_by_y[y], y)]

        PlotFactory2.set_points(self._plot_widget, points=points, color='red')

        self._result_label.setText('Incorrecto. Los dos puntos indicados muestran porque la gráfica no tiene inversa.')
        self._result_label.setStyleSheet('color: red')
        self._result_label.setVisible(True)

    def _setup_finished_exercise(self):
        super(InverseDelimitedComponent, self)._setup_finished_exercise()
        self._region.setMovable(False)

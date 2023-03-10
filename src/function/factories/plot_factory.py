from typing import List

import pyqtgraph
from PyQt5.QtGui import QFont
from pyqtgraph import TextItem

from src.function.models import Function, FunctionExercise, Point


class PlotFactory:
    @classmethod
    def get_plot(cls, functions: List[Function], exercise: FunctionExercise, show_title: bool = False,
                 show_ends: bool = True, rgb_tuple=None, show_grid: bool = True, parent=None) -> pyqtgraph.PlotWidget:
        graph = pyqtgraph.PlotWidget() if not parent else pyqtgraph.PlotWidget(parent)
        graph.setFixedSize(650, 650)
        graph.setMouseEnabled(x=False, y=False)
        graph.showGrid(x=show_grid, y=show_grid)

        colors = [(255, 255, 255), (255, 255, 0), (128, 0, 128), (255, 153, 51), (255, 51, 204)]
        function_ranges = []
        has_multiple_main_graphics = len([function for function in functions if function.is_main_graphic]) > 1
        for function in functions:
            x_values, y_values = function.x_values, function.y_values
            pen = pyqtgraph.mkPen(color=colors.pop(0), width=5) \
                if function.is_main_graphic and not has_multiple_main_graphics \
                else pyqtgraph.mkPen(color=colors.pop(), width=3)
            pen = pen if not rgb_tuple else pyqtgraph.mkPen(color=rgb_tuple, width=5)
            graph.plot(x_values, y_values, pen=pen)

            if show_title and function.is_elementary_graph and function.is_main_graphic and len(functions) == 1:
                math_expression = function.get_math_expression()
                graph.setTitle(math_expression, color='yellow', size='18pt')

            function_ranges.append((x_values, y_values))

            if show_ends:
                is_first_point_included = function.domain[0] == '['
                first_point_filling = 'w' if is_first_point_included else 'black'
                graph.plot([x_values[0]], [y_values[0]], symbol='o', symbolBrush=first_point_filling, symbolSize='12')

                is_last_point_included = function.domain[-1] == ']'
                last_point_filling = 'w' if is_last_point_included else 'black'
                graph.plot([x_values[-1]], [y_values[-1]], symbol='o', symbolBrush=last_point_filling, symbolSize='12')

        plot_x_range = plot_y_range = exercise.exercise_domain if exercise.exercise_domain else (-5, 5)
        graph.setRange(xRange=plot_x_range, yRange=plot_y_range)
        graph.getAxis('left').setTextPen('yellow')
        graph.getAxis('bottom').setTextPen('yellow')
        return graph

    @classmethod
    def update_plot(cls, plot_widget: pyqtgraph.PlotWidget, functions_to_update: List[Function],
                    help_points: List[Point] = None, is_help_data: bool = False,
                    rgb_tuple: tuple = (0, 0, 255), no_points: bool = False, constants: bool = False,
                    show_ends: bool = True):
        if not help_points:
            help_points = []

        for function in functions_to_update:
            pen_width = 1 if is_help_data else 3
            pen = pyqtgraph.mkPen(color=rgb_tuple, width=pen_width) if is_help_data \
                else pyqtgraph.mkPen(color=rgb_tuple, width=pen_width)

            x_values, y_values = function.get_points() if not constants else function.get_constant_points()
            plot_widget.plot(x_values, y_values, pen=pen)

            if no_points:
                continue

            if not show_ends:
                continue

            is_first_point_included = function.domain[0] == '['
            first_point_filling = 'w' if is_first_point_included else 'black'
            plot_widget.plot([x_values[0]], [y_values[0]], symbol='o', symbolBrush=first_point_filling, symbolSize='12')

            is_last_point_included = function.domain[-1] == ']'
            last_point_filling = 'w' if is_last_point_included else 'black'
            plot_widget.plot([x_values[-1]], [y_values[-1]], symbol='o', symbolBrush=last_point_filling,
                             symbolSize='12')

        for point in help_points:
            plot_widget.plot([point.x_value], [point.y_value], symbol='o', symbolBrush=rgb_tuple, symbolSize='12')

    @classmethod
    def update_plot_with_points(cls, plot_widget: pyqtgraph.PlotWidget, point_function: List[List[tuple]],
                                no_points: bool = False, rgb_tuple: tuple = (0, 0, 255), included: bool = False,
                                point_color: tuple = (0, 0, 255), pen_width: int = None):

        for function in point_function:
            pen_width = 3 if not pen_width else pen_width
            pen = pyqtgraph.mkPen(color=rgb_tuple, width=pen_width)

            x_values = [point[0] for point in function]
            y_values = [point[1] for point in function]
            plot_widget.plot(x_values, y_values, pen=pen)

            if no_points:
                continue

            plot_widget.plot([x_values[0]], [y_values[0]], symbol='o', symbolBrush=point_color, symbolSize='12')
            plot_widget.plot([x_values[-1]], [y_values[-1]], symbol='o', symbolBrush=point_color, symbolSize='12')

    @classmethod
    def add_function_labels(cls, plot_widget: pyqtgraph.PlotWidget, functions_to_labelling_with_color: list):
        positions = ['left', 'right', 'left_plus', 'right_plus']
        for function, color in functions_to_labelling_with_color:
            font = QFont()
            font.setPixelSize(25)
            x_value, y_value = function.get_label_point(position=positions.pop(0))
            label = TextItem(anchor=(0.5, 0.5))
            text = function.get_math_expression()
            label.setText(text=text)
            label.setPos(x_value - 0.2, y_value + 0.4)
            label.setFont(font)
            label.setColor(color)
            plot_widget.addItem(label)

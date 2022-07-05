from typing import List

import pyqtgraph
from PyQt5.QtGui import QFont
from pyqtgraph import TextItem

from src.function.models.function import Function
from src.function.models.function_point import FunctionPoint


class PlotFactory:
    @classmethod
    def get_plot(cls, functions: List[Function], show_title: bool = False,
                 show_ends: bool = True) -> pyqtgraph.PlotWidget:
        graph = pyqtgraph.PlotWidget()
        graph.setMouseEnabled(x=False, y=False)
        graph.showGrid(x=True, y=True)

        function_ranges = []
        for function in functions:
            x_values, y_values = function.get_points()
            pen = pyqtgraph.mkPen(color=(255, 255, 255), width=5) if function.is_main_graphic \
                else pyqtgraph.mkPen(color=(128, 0, 128), width=3)
            graph.plot(x_values, y_values, pen=pen)
            if show_title and function.is_elementary_graph and function.is_main_graphic and len(functions) == 1:
                math_expression = function.get_math_expression()
                graph.setTitle(math_expression, color='orange', size='18pt')

            function_ranges.append((x_values, y_values))

            if show_ends:
                is_first_point_included = function.domain[0] == '['
                first_point_filling = 'w' if is_first_point_included else 'black'
                graph.plot([x_values[0]], [y_values[0]], symbol='o', symbolBrush=first_point_filling, symbolSize='12')

                is_last_point_included = function.domain[-1] == ']'
                last_point_filling = 'w' if is_last_point_included else 'black'
                graph.plot([x_values[-1]], [y_values[-1]], symbol='o', symbolBrush=last_point_filling, symbolSize='12')

        plot_x_range = plot_y_range = (-5, 5)
        graph.setRange(xRange=plot_x_range, yRange=plot_y_range)
        return graph

    @classmethod
    def update_plot(cls, plot_widget: pyqtgraph.PlotWidget, functions_to_update: List[Function],
                    help_points: List[FunctionPoint] = None, is_help_data: bool = False,
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
            color = 'blue'
            plot_widget.plot([point.x_value], [point.y_value], symbol='o', symbolBrush=color, symbolSize='12')

        plot_x_range = plot_y_range = (-5, 5)
        plot_widget.setRange(xRange=plot_x_range, yRange=plot_y_range)

    @classmethod
    def add_function_labels(cls, plot_widget: pyqtgraph.PlotWidget, functions_to_labelling_with_color: list):
        for function, color in functions_to_labelling_with_color:
            font = QFont()
            font.setPixelSize(20)
            x_value, y_value = function.get_random_points()
            label = TextItem(anchor=(0.5, 0.5))
            text = function.get_math_expression()
            label.setText(text=text)
            label.setPos(x_value - 0.2, y_value + 0.4)
            label.setFont(font)
            label.setColor(color)
            plot_widget.addItem(label)

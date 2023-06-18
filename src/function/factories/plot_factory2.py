import math
from typing import List, Tuple

import pyqtgraph
from PyQt5.QtGui import QFont
from pyqtgraph import TextItem

from src.function.models import Function, Point


class PlotFactory2:
    @classmethod
    def get_plot(cls, parent=None, show_grid: bool = True,
                 function_range: Tuple[int, int] = (5, 5)) -> pyqtgraph.PlotWidget:
        graph = pyqtgraph.PlotWidget() if not parent else pyqtgraph.PlotWidget(parent)
        graph.setFixedSize(650, 650)
        graph.setMenuEnabled(False)
        graph.customContextMenuRequested.connect(lambda: None)
        graph.setMouseEnabled(x=False, y=False)
        graph.showGrid(x=show_grid, y=show_grid)
        graph.getAxis('left').setTextPen('yellow')
        graph.getAxis('bottom').setTextPen('yellow')

        graph_range = (function_range[0] + 0.4, function_range[1] - 0.4)
        graph.setRange(xRange=graph_range, yRange=graph_range)

        graph.plotItem.setLimits(xMin=function_range[0], xMax=function_range[1])
        graph.plotItem.setLimits(yMin=function_range[0], yMax=function_range[1])
        return graph

    @classmethod
    def set_functions(cls, graph: pyqtgraph.PlotWidget, functions: List[Function], function_width: int = 3,
                      color: [str, Tuple] = '', show_limits: bool = False, click_function=None) -> None:
        # pink red green blue
        colors = [(255, 0, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255)]
        for function in functions:
            x_values, y_values = function.x_values, function.y_values
            for x_set, y_set in zip(x_values, y_values):
                color_selected = color if color else colors.pop()
                PlotFactory2.set_graph_using_points(
                    graph=graph, x_values=x_set, y_values=y_set, color=color_selected,
                    function_width=function_width,
                    function_name=function.expression, click_function=click_function
                )

            if show_limits:
                PlotFactory2._setup_limits(graph=graph, function=function, x_values=x_values, y_values=y_values)

    @classmethod
    def _setup_limits(cls, graph: pyqtgraph.PlotWidget, function: Function, x_values: List[int], y_values: List[int]):
        if '-inf' not in function.domain:
            is_first_point_included = function.domain[0] == '['
            first_point_filling = 'w' if is_first_point_included else 'black'
            graph.plot([x_values[0][0]], [y_values[0][0]], symbol='o', symbolBrush=first_point_filling, symbolSize='12')

        if '+inf' not in function.domain:
            is_last_point_included = function.domain[-1] == ']'
            last_point_filling = 'w' if is_last_point_included else 'black'
            graph.plot([x_values[-1][-1]], [y_values[-1][-1]], symbol='o', symbolBrush=last_point_filling,
                       symbolSize='12')

    @classmethod
    def set_points(cls, graph: pyqtgraph.PlotWidget, points: List[Point], color: [str, tuple] = '') -> None:
        for point in points:
            graph.plot([point.x], [point.y], symbol='o', symbolBrush=color, symbolSize='12')

    @classmethod
    def set_graph_using_points(cls, graph: pyqtgraph.PlotWidget, x_values: List[int], y_values: List[int],
                               color: [str, Tuple] = 'yellow', function_width: float = 3, function_name: str = '',
                               click_function=None):
        pen = pyqtgraph.mkPen(color=color, width=function_width)
        plot_data_item = graph.plot(x_values, y_values, pen=pen, name=function_name)

        if click_function:
            plot_data_item.setCurveClickable(state=2, width=10)
            plot_data_item.curve.sigClicked.connect(click_function)
            plot_data_item.curve.metaData['name'] = function_name
        return plot_data_item

    @classmethod
    def set_labels2(cls, graph: pyqtgraph.PlotWidget, points: List[Tuple[Point, Tuple[tuple, str]]]) -> None:
        for point, point_info in points:
            color, text = point_info
            x_value, y_value = point.x, point.y
            font = QFont()
            font.setPixelSize(25)
            label = TextItem(anchor=(0.5, 0.5))
            label.setText(text=text)
            label.setPos(x_value, y_value)
            label.setFont(font)
            label.setColor(color)
            graph.addItem(label)

    @classmethod
    def set_labels(cls, graph: pyqtgraph.PlotWidget, functions: list) -> None:
        points_added = set()
        for function, color in functions:
            font = QFont()
            font.setPixelSize(25)
            points = function.get_label_point()
            point = (points[0][0], points[0][1])
            for p in points:
                can_use_point = False
                for p1 in points_added:
                    result = abs(p1[0] - p[0]) + abs(p1[1] - p[1]) > 0.5
                    if result:
                        can_use_point = True
                if can_use_point or not points_added:
                    point = p
                    points_added.add(point)
                    break
            points_added.add(point)
            label = TextItem(anchor=(0.5, 0.5))
            text = function.get_math_expression()
            label.setText(text=text)
            label.setPos(point[0], point[1])
            label.setFont(font)
            label.setColor(color)
            graph.addItem(label)

    @classmethod
    def reset_graph(cls, graph: pyqtgraph.PlotWidget):
        graph.plotItem.clear()

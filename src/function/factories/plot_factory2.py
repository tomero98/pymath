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
        graph.setMouseEnabled(x=False, y=False)
        graph.showGrid(x=show_grid, y=show_grid)
        graph.getAxis('left').setTextPen('yellow')
        graph.getAxis('bottom').setTextPen('yellow')
        graph.setRange(xRange=function_range, yRange=function_range)
        return graph

    @classmethod
    def set_functions(cls, graph: pyqtgraph.PlotWidget, functions: List[Function], function_width: int = 3,
                      color: str = 'blue', show_limits: bool = False) -> None:
        colors = [(255, 255, 255), (255, 255, 0), (128, 0, 128), (255, 153, 51), (255, 51, 204)]
        for function in functions:
            x_values, y_values = function.x_values, function.y_values
            color_selected = color if color else colors.pop()
            pen = pyqtgraph.mkPen(color=color_selected, width=function_width)
            graph.plot(x_values, y_values, pen=pen)

            if show_limits:
                is_first_point_included = function.domain[0] == '['
                first_point_filling = 'w' if is_first_point_included else 'black'
                graph.plot([x_values[0]], [y_values[0]], symbol='o', symbolBrush=first_point_filling, symbolSize='12')

                is_last_point_included = function.domain[-1] == ']'
                last_point_filling = 'w' if is_last_point_included else 'black'
                graph.plot([x_values[-1]], [y_values[-1]], symbol='o', symbolBrush=last_point_filling, symbolSize='12')

    @classmethod
    def set_points(cls, graph: pyqtgraph.PlotWidget, points: List[Point], color: str = '') -> None:
        for point in points:
            graph.plot([point.x], [point.y], symbol='o', symbolBrush=color, symbolSize='12')

    @classmethod
    def set_labels(cls, graph: pyqtgraph.PlotWidget, functions: list) -> None:
        for function, color in functions:
            font = QFont()
            font.setPixelSize(25)
            x_value, y_value = function.get_label_point()
            label = TextItem(anchor=(0.5, 0.5))
            text = function.get_math_expression()
            label.setText(text=text)
            label.setPos(x_value - 0.2, y_value + 0.4)
            label.setFont(font)
            label.setColor(color)
            graph.addItem(label)

    @classmethod
    def reset_graph(cls, graph: pyqtgraph.PlotWidget):
        graph.plotItem.clear()

from typing import List

import pyqtgraph

from src.function.models.function import Function


class PlotFactory:
    @classmethod
    def get_plot(cls, functions: List[Function]) -> pyqtgraph.PlotWidget:
        graph = pyqtgraph.PlotWidget()
        graph.setMouseEnabled(x=False, y=False)
        graph.showGrid(x=True, y=True)

        function_ranges = []
        for function in functions:
            x_values, y_values = function.get_points()
            pen = pyqtgraph.mkPen(color=(255, 255, 255)) if function.is_main_graphic \
                else pyqtgraph.mkPen(color=(128, 0, 128))
            graph.plot(x_values, y_values, pen=pen)

            function_ranges.append((x_values, y_values))
            if not function.domain:
                continue

            # function_ranges.append((x_values, y_values))
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
    def update_plot(cls, plot_widget: pyqtgraph.PlotWidget, current_functions: List[Function],
                    functions_to_update: List[Function], is_help_data: bool = False):
        function_ranges = []
        for function in functions_to_update:
            pen = pyqtgraph.mkPen(color=(0, 0, 255)) if is_help_data else pyqtgraph.mkPen(color=(255, 0, 0))

            x_values, y_values = function.get_points()
            plot_widget.plot(x_values, y_values, pen=pen)

            if not function.domain:
                continue

            function_ranges.append((x_values, y_values))
            is_first_point_included = function.domain[0] == '['
            first_point_filling = 'w' if is_first_point_included else 'black'
            plot_widget.plot([x_values[0]], [y_values[0]], symbol='o', symbolBrush=first_point_filling, symbolSize='12')

            is_last_point_included = function.domain[-1] == ']'
            last_point_filling = 'w' if is_last_point_included else 'black'
            plot_widget.plot([x_values[-1]], [y_values[-1]], symbol='o', symbolBrush=last_point_filling,
                             symbolSize='12')

        current_ranges = [function.get_points() for function in current_functions]
        plot_x_range, plot_y_range = cls._get_range_functions(function_ranges=function_ranges + current_ranges)
        plot_widget.setRange(xRange=plot_x_range, yRange=plot_y_range)

    @staticmethod
    def _get_range_functions(function_ranges: (tuple, tuple)) -> (tuple, tuple):
        graph_min_x = graph_max_x = graph_min_y = graph_max_y = 5
        for x_values, y_values in function_ranges:
            function_min_x, function_max_x = min(x_values), max(x_values),
            function_min_y, function_max_y = min(y_values), max(y_values)
            graph_min_x = function_min_x if graph_min_x is None or graph_min_x > function_min_x else graph_min_x
            graph_max_x = function_max_x if graph_max_x is None or graph_max_x < function_max_x else graph_max_x
            graph_min_y = function_min_y if graph_min_y is None or graph_min_y > function_min_y else graph_min_y
            graph_max_y = function_max_y if graph_max_y is None or graph_max_y < function_max_y else graph_max_y

        x_distance = abs(graph_min_x - graph_max_x) * 0.5
        y_distance = abs(graph_min_y - graph_max_y) * 0.5
        plot_x_range = (graph_min_x - x_distance, graph_max_x + x_distance)
        plot_y_range = (graph_min_y - y_distance, graph_max_y + y_distance)
        return plot_x_range, plot_y_range

# Puntos en la grafica
# x_points_plot = [x for x, y in zip(x_values[1:-1], y_values[1:-1]) if x == int(x) and y == int(y)]
# y_points_plot = [y for x, y in zip(x_values[1:-1], y_values[1:-1]) if x == int(x) and y == int(y)]
# graph.plot(x_points_plot, y_points_plot, symbol='o', symbolBrush='w', symbolSize='5')

# Setup coordenadas
# self.proxy = pyqtgraph.SignalProxy(graph.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved)
# def mouseMoved(self, e):
#     pos = e[0]
#     if self._plot_widget.sceneBoundingRect().contains(pos):
#         mousePoint = self._plot_widget.getPlotItem().vb.mapSceneToView(pos)
#         x_position = round(mousePoint.x(), 1)
#         y_position = round(mousePoint.y(), 1)
#         position_text = f'Posición actual: ({x_position}, {y_position})'
#         # self._help_subtitle_widget.setText(position_text)
#
#         if x_position == int(x_position) and y_position == int(y_position):
#             x_values, y_values = self._exercise.functions[0].get_points()
#             dictionary = {x: y for x, y in zip(x_values, y_values)}
#             if x_position in x_values and y_position in y_values and dictionary[x_position] == y_position:
#                 QApplication.setOverrideCursor(Qt.PointingHandCursor)
#         else:
#             QApplication.restoreOverrideCursor()

# Add labels
# font = QFont()
# font.setPixelSize(9)
# label = TextItem(anchor=(0.5,0.5))
# label.setText(text='Ejemplo de todo')
# label.setPos(0, 0)
# label.setFont(font)
# graph.addItem(label)

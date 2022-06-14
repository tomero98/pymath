import sys

from src.projectConf.app import Controller
from src.projectConf.database.database_manager import DatabaseManager

if not __name__ == '__main__':
    database_manager = DatabaseManager()
    database_manager.setup_database()
    controller = Controller()
    sys.exit(controller.run())

from PyQt5 import QtWidgets
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)

        hour = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        temperature = [30, -32, 34, 32, -33, 31, 29, 32, 35, 45]

        '[2, 5)'

        # plot data: x, y values
        self.graphWidget.setTitle("Title")
        self.graphWidget.setBackground('w')
        self.graphWidget.showGrid(x=True, y=True)
        pen = pg.mkPen(color=(255, 0, 0))
        line = self.graphWidget.plot(hour, temperature, pen=pen)
        line.scatter.setData(x=[1], y=[30])
        # hour = [1]
        # temperature = [55]
        # line = self.graphWidget.plot(hour, temperature, pen=None,
        #       name="BEP",
        #       symbol='o',
        #       symbolPen=pg.mkPen(color='w', width=0),
        #       # symbolBrush=pg.mkBrush(0, 0, 255, 255),
        #       symbolSize=7)
        # line.setSymbol('o')
        pg.plot([1, 1, 1, 1, 1], pen=(0, 0, 0), symbolBrush=None,
                symbolPen='w', symbol='o', symbolSize=10, name="symbol ='o'")


# importing Qt widgets
from PyQt5.QtWidgets import *

# importing system
import sys

# importing numpy as np
import numpy as np

# importing pyqtgraph as pg
import pyqtgraph as pg
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Window(QMainWindow):

    def __init__(self):
        super().__init__()

        # setting title
        self.setWindowTitle("PyQtGraph")

        # setting geometry
        self.setGeometry(100, 100, 600, 500)

        # icon
        icon = QIcon("skin.png")

        # setting icon to the window
        self.setWindowIcon(icon)

        # calling method
        self.UiComponents()

        # showing all the widgets
        self.show()

    # method for components
    def UiComponents(self):
        # creating a widget object
        widget = QWidget()

        # creating a label
        label = QLabel("Geeksforgeeks Scatter Plot")

        # making label do word wrap
        label.setWordWrap(True)

        # creating a plot window
        plot = pg.plot()

        # number of points
        n = 300

        # creating a scatter plot item
        # of size = 10
        # using brush to enlarge the of green color
        scatter = pg.ScatterPlotItem(
            size=10, brush=pg.mkBrush(30, 255, 35, 255))

        # data for x-axis
        x_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        # data for y-axis
        y_data = [5, 4, 6, 4, 3, 5, 6, 6, 7, 8]

        # setting data to the scatter plot
        scatter.setData(x_data, y_data)

        # add item to plot window
        # adding scatter plot item to the plot window
        plot.addItem(scatter)

        # Creating a grid layout
        layout = QGridLayout()

        # minimum width value of the label
        label.setMinimumWidth(130)

        # setting this layout to the widget
        widget.setLayout(layout)

        # adding label in the layout
        layout.addWidget(label, 1, 0)

        # plot window goes on right side, spanning 3 rows
        layout.addWidget(plot, 0, 1, 3, 1)

        # setting this widget as central widget of the main window
        self.setCentralWidget(widget)

        # setting tool tip to the scatter plot
        scatter.setToolTip("This is tip")

        # getting tool tip of scatter plot
        value = scatter.toolTip()

        # setting text to the value
        label.setText("Tool tip : " + str(value))


# create pyqt5 app
App = QApplication(sys.argv)

# create the instance of our Window
window = Window()

# start the app
sys.exit(App.exec())
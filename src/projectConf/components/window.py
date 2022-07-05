import sys

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QMenu, QAction


class Window(QMainWindow):
    continue_signal = pyqtSignal()
    close_signal = pyqtSignal()

    def __init__(self, title):
        super().__init__()
        self.setFixedSize(1400, 875)
        self.setWindowTitle(title)
        self.setStyleSheet("background-color: white;")
        self.center()
        self._create_menu_bar()

    def _create_menu_bar(self):
        menu_bar = self.menuBar()
        menu_bar.setStyleSheet('background-color: grey')
        file_menu = QMenu("&File", self)
        exit_action = QAction("&Exit", self)
        exit_action.triggered.connect(self._exit_app)
        file_menu.addAction(exit_action)
        menu_bar.addMenu(file_menu)

    def _exit_app(self):
        sys.exit(0)

    def draw(self, *args, **kwargs):
        pass

    def center(self):
        window_geometry = self.frameGeometry()
        screen_center_point = QDesktopWidget().availableGeometry().center()
        window_geometry.moveCenter(screen_center_point)
        self.move(window_geometry.topLeft())

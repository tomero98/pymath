import sys

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget


class Window(QMainWindow):
    continue_signal = pyqtSignal()
    close_signal = pyqtSignal()

    def __init__(self, title):
        super().__init__()
        self.setFixedSize(1200, 1000)
        self.setWindowTitle(title)
        self.setObjectName('application')
        self.setStyleSheet("""
        QWidget#application {
            background-color: #EDEDE9;
        }
        
        #container {
            border: 4px solid #897B6D;
            border-radius: 20px;
            background: #F5EBE0;
        }
        
        #topic-container {
            border: 4px solid #897B6D;
            border-radius: 20px;
            background: #F5EBE0;
        }
            
        #topic-container::hover {
            border: 5px solid #897B6D;
        }
        """)
        self.center()

    def _exit_app(self):
        sys.exit(0)

    def draw(self, *args, **kwargs):
        pass

    def center(self):
        window_geometry = self.frameGeometry()
        screen_center_point = QDesktopWidget().availableGeometry().center()
        window_geometry.moveCenter(screen_center_point)
        self.move(window_geometry.topLeft())

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout


class UserStatsDialog(QWidget):
    close_signal = pyqtSignal()

    def __init__(self):
        super(UserStatsDialog, self).__init__()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.close_signal.emit()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close_signal.emit()

    def draw(self):
        self.setObjectName('application')
        self.setStyleSheet("""
                    QWidget#application {
                        background-color: #EDEDE9;
                    }"""
                           )
        self.setWindowTitle('Configuración del ejercicio')

        layout = QVBoxLayout()

        self._get_user_stats_layout()

        self.setLayout(layout)
        self.show()
        self.setFixedSize(self.width(), self.height())

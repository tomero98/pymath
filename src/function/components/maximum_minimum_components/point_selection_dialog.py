from PyQt5 import QtGui
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QComboBox, QPushButton

from src.projectConf.factories import ButtonFactory, LabelFactory
from src.projectConf.models.enums import TextType
from ...models import Point


class PointSelectionDialog(QWidget):
    continue_signal = pyqtSignal(str, Point)
    close_signal = pyqtSignal()

    def __init__(self, point: Point):
        super(PointSelectionDialog, self).__init__()

        self._point = point

        self._point_selection_combobox: QComboBox = None  # noqa
        self._continue_button: QPushButton = None  # noqa

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.close_signal.emit()

    def draw(self):
        self.setWindowTitle('Selección del punto')

        layout = QVBoxLayout()

        text_label = LabelFactory.get_label_component(
            text=f'Indica el tipo para el punto {str(self._point)}: ', label_type=TextType.NORMAL_TEXT,
            align=Qt.AlignHCenter, need_word_wrap=True, set_visible=True
        )
        layout.addWidget(text_label, alignment=Qt.AlignHCenter)

        self._point_selection_combobox = QComboBox()
        self._point_selection_combobox.addItem('máximo absoluto')
        self._point_selection_combobox.addItem('máximo relativo')
        self._point_selection_combobox.addItem('mínimo absoluto')
        self._point_selection_combobox.addItem('mínimo relativo')
        self._point_selection_combobox.adjustSize()
        layout.addWidget(self._point_selection_combobox, alignment=Qt.AlignHCenter)

        self._continue_button = ButtonFactory.get_button_component(
            title='Continuar', minimum_width=45, minimum_height=45, text_size=22, tooltip='Continuar',
            function_to_connect=self._send_signal
        )

        layout.addWidget(self._continue_button, alignment=Qt.AlignHCenter)

        self.setLayout(layout)
        self.show()
        self.setFixedSize(self.width() + 50, self.height())

    def _send_signal(self):
        self.continue_signal.emit(self._point_selection_combobox.currentText(), self._point)


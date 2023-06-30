from PyQt5 import QtGui
from PyQt5.QtCore import Qt, pyqtSignal, QRegExp
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QComboBox, QPushButton, QLineEdit, QHBoxLayout

from src.projectConf.factories import ButtonFactory, LabelFactory, LineEditFactory, IconFactory
from src.projectConf.models.enums import TextType
from ...models import Point


class PointSelectionDialog(QWidget):
    continue_signal = pyqtSignal(str, Point, str, str)
    close_signal = pyqtSignal()

    def __init__(self, point: Point):
        super(PointSelectionDialog, self).__init__()

        self._point: Point = point
        self._range_pattern: str = r'(^\(|\[){1}(-?\d+(\.\d+)?),\s(-?\d+(\.\d+)?)(\]|\)){1}$'
        self._point_pattern: str = r"\(-?\d+(\.\d+)?,\s*-?\d+(\.\d+)?\)"
        self._y_pattern: str = r"[-+]?\d+(\.\d{1,2})?"

        self._point_selection_combobox: QComboBox = None  # noqa
        self._continue_button: QPushButton = None  # noqa
        self._point_edition_edit: QLineEdit = None  # noqa
        self._y_edition_edit: QLineEdit = None  # noqa
        self._range_edition_edit: QLineEdit = None  # noqa

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close_signal.emit()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.close_signal.emit()

    def draw(self):
        self.setObjectName('application')
        self.setStyleSheet("""
                QWidget#application {
                    background-color: #EDEDE9;
                }
            """
                           )
        self.setWindowTitle('Selección del punto')

        widget = QWidget()
        widget.setObjectName('topic-container')
        widget.setStyleSheet("""
            #topic-container {
                border: 4px solid #897B6D;
                border-radius: 20px;
                background: #F5EBE0;
            }
        """)

        layout = QVBoxLayout()
        layout1 = QVBoxLayout()

        point_edition_layout = QHBoxLayout()
        text_label = LabelFactory.get_label_component(
            text=f'El punto introducido es el siguiente:', label_type=TextType.NORMAL_TEXT, set_visible=True
        )
        self._point_edition_edit = LineEditFactory.get_line_edit_component(
            placeholder_text='(2, 3)', font_size=TextType.NORMAL_TEXT.value
        )
        self._point_edition_edit.setText(str(self._point))
        regex = QRegExp(self._point_pattern)
        validator = QtGui.QRegExpValidator(regex)
        self._point_edition_edit.setValidator(validator)
        point_edition_layout.addWidget(text_label)
        point_edition_layout.addWidget(self._point_edition_edit)
        layout.addLayout(point_edition_layout)

        text_label = LabelFactory.get_label_component(
            text=f'Puedes introducir también un rango de valores:', label_type=TextType.NORMAL_TEXT, set_visible=True
        )
        layout.addWidget(text_label)

        y_edition_layout = QHBoxLayout()
        text_label = LabelFactory.get_label_component(
            text=f'Valor de la ordenada:', label_type=TextType.NORMAL_TEXT, set_visible=True
        )
        self._y_edition_edit = LineEditFactory.get_line_edit_component(
            placeholder_text='-1.5', font_size=TextType.NORMAL_TEXT.value
        )
        regex = QRegExp(self._y_pattern)
        validator = QtGui.QRegExpValidator(regex)
        self._y_edition_edit.setValidator(validator)
        y_edition_layout.addWidget(text_label)
        y_edition_layout.addWidget(self._y_edition_edit)

        text_label = LabelFactory.get_label_component(
            text=f'Rango de valores:', label_type=TextType.NORMAL_TEXT, set_visible=True
        )
        self._range_edition_edit = LineEditFactory.get_line_edit_component(
            placeholder_text='[2, 5)', font_size=TextType.NORMAL_TEXT.value
        )
        regex = QRegExp(self._range_pattern)
        validator = QtGui.QRegExpValidator(regex)
        self._range_edition_edit.setValidator(validator)
        y_edition_layout.addWidget(text_label)
        y_edition_layout.addWidget(self._range_edition_edit)

        layout.addLayout(y_edition_layout)

        self._point_selection_combobox = QComboBox()
        self._point_selection_combobox.addItem('máximo absoluto')
        self._point_selection_combobox.addItem('máximo relativo')
        self._point_selection_combobox.addItem('mínimo absoluto')
        self._point_selection_combobox.addItem('mínimo relativo')
        self._point_selection_combobox.adjustSize()
        self._point_selection_combobox.setStyleSheet('background-color: #ECDAC6;')

        layout.addWidget(self._point_selection_combobox, alignment=Qt.AlignHCenter)

        icon = IconFactory.get_icon_widget(image_name='check_exercise.png')
        self._continue_button = ButtonFactory.get_button_component(
            title='', function_to_connect=self._send_signal, primary_button=True, icon=icon,
            icon_size=45, tooltip='Continuar'
        )

        layout.addWidget(self._continue_button, alignment=Qt.AlignHCenter)

        widget.setLayout(layout)
        layout1.addWidget(widget)
        self.setLayout(layout1)
        self.show()
        self.setFixedSize(self.width() + 50, self.height())

    def _send_signal(self):
        selected_point = self._point_edition_edit.text()
        if selected_point:
            x_point = float(selected_point[1:-1].split(',')[0])
            y_point = float(selected_point[1:-1].split(',')[-1])
            point = Point(x=x_point, y=y_point)
        else:
            point = Point(x=None, y=None)
        self.continue_signal.emit(self._point_selection_combobox.currentText(), point,
                                  self._y_edition_edit.text(), self._range_edition_edit.text())

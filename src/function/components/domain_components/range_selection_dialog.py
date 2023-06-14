import re

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, pyqtSignal, QRegExp
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel

from src.projectConf.factories import ButtonFactory, LabelFactory, IconFactory, LineEditFactory
from src.projectConf.models.enums import TextType


class RangeSelectionDialog(QWidget):
    continue_signal = pyqtSignal(str)
    delete_signal = pyqtSignal()

    default_text = 'Se espera una única expresión de la siguiente forma: (-inf, 3], (1, 2), [0, +inf)'

    def __init__(self, plot_range: list, ranges_added: list, range_item: str = None):
        super(RangeSelectionDialog, self).__init__()

        self._pattern: str = r'(^\(|\[){1}(-inf|-?\d+(\.\d+)?),\s(-?\d+(\.\d+)?|\+inf)(\]|\)){1}$'
        self._plot_range = plot_range
        self._ranges_added: list = ranges_added
        self._range_item: str = range_item

        self._continue_button: QPushButton = None  # noqa
        self._range_edition: QLineEdit = None  # noqa
        self._range_edition_help_text: QLabel = None  # noqa

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.delete_signal.emit()

    def draw(self):
        self.setWindowTitle('Selecciona el rango')

        layout = QVBoxLayout()

        if self._range_item:
            text = f'Editar el rango {self._range_item}'
        else:
            text = 'Crear nuevo rango de valores'
        text_label = LabelFactory.get_label_component(
            text=text, label_type=TextType.SUBTITLE, align=Qt.AlignHCenter, need_word_wrap=False, set_visible=True
        )

        answer_layout = self._get_answer_layout()

        self._range_edition_help_text = LabelFactory.get_label_component(
            text=self.default_text, label_type=TextType.SMALL_TEXT, align=Qt.AlignLeft, set_visible=True
        )
        self._range_edition_help_text.setStyleSheet('color: black;')

        layout.addWidget(text_label, alignment=Qt.AlignTop | Qt.AlignLeft)
        layout.addLayout(answer_layout)
        layout.addWidget(self._range_edition_help_text, alignment=Qt.AlignRight)

        self.setLayout(layout)
        self.show()
        self.setFixedSize(self.width(), self.height())

    def _get_answer_layout(self) -> QHBoxLayout:
        layout = QHBoxLayout()

        text_label = LabelFactory.get_label_component(
            text=f'Indica el rango a introducir:', label_type=TextType.NORMAL_TEXT, align=Qt.AlignHCenter,
            need_word_wrap=False, set_visible=True
        )

        range_edition_layout = self._get_range_edition_layout()

        icon = IconFactory.get_icon_widget(image_name='tick.png')
        self._continue_button = ButtonFactory.get_button_component(
            title='', function_to_connect=self._send_signal, icon=icon, icon_size=25, tooltip='Aceptar',
            primary_button=True
        )
        self._continue_button.setDisabled(True)

        layout.addWidget(text_label, alignment=Qt.AlignVCenter)
        layout.addLayout(range_edition_layout)
        layout.addWidget(self._continue_button, alignment=Qt.AlignVCenter)

        return layout

    def _get_range_edition_layout(self) -> QVBoxLayout:
        layout = QVBoxLayout()

        self._range_edition = LineEditFactory.get_line_edit_component(
            placeholder_text='(-inf, 3]', fixed_height=30, fixed_width=300, font_size=TextType.NORMAL_TEXT.value
        )
        if self._range_item:
            self._range_edition.setText(self._range_item)

        self._range_edition.textChanged.connect(self._check_range_edition)

        regex = QRegExp(self._pattern)
        validator = QtGui.QRegExpValidator(regex)
        self._range_edition.setValidator(validator)

        layout.addWidget(self._range_edition)
        return layout

    def _send_signal(self):
        self.continue_signal.emit(self._range_edition.text())

    def _check_range_edition(self):
        match = re.match(self._pattern, self._range_edition.text())
        if match:
            first_limit = match.group(1)
            lower_limit = float(match.group(2))
            upper_limit = float(match.group(4))
            last_limit = match.group(6)

            if lower_limit == float('-inf'):
                if first_limit == '[':
                    self._continue_button.setDisabled(True)
                    self._range_edition_help_text.setText('Se está incluyendo -inf en el rango.')
                    self._range_edition_help_text.setStyleSheet('color: red;')
                    return None

            if upper_limit == float('inf'):
                if last_limit == ']':
                    self._continue_button.setDisabled(True)
                    self._range_edition_help_text.setText('Se está incluyendo +inf en el rango.')
                    self._range_edition_help_text.setStyleSheet('color: red;')
                    return None

            if lower_limit >= upper_limit:
                self._continue_button.setDisabled(True)
                self._range_edition_help_text.setText('El límite inferior es mayor o igual que el límite mayor.')
                self._range_edition_help_text.setStyleSheet('color: red;')
                return None

            if not lower_limit == float('-inf') and lower_limit < self._plot_range[0]:
                self._continue_button.setDisabled(True)
                self._range_edition_help_text.setText(
                    'El límite inferior es menor que el rango mostrado en la gráfica.'
                )
                self._range_edition_help_text.setStyleSheet('color: red;')
                return None

            if not upper_limit == float('inf') and upper_limit > self._plot_range[1]:
                self._continue_button.setDisabled(True)
                self._range_edition_help_text.setText(
                    'El límite superior es mayor que el rango mostrado en la gráfica.'
                )
                self._range_edition_help_text.setStyleSheet('color: red;')
                return None

            self._continue_button.setDisabled(False)
            self._range_edition_help_text.setText(self.default_text)
            self._range_edition_help_text.setStyleSheet('color: black;')
            return None

        self._continue_button.setDisabled(True)
        self._range_edition_help_text.setText(self.default_text)
        self._range_edition_help_text.setStyleSheet('color: black;')

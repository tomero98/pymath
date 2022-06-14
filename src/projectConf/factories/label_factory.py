from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel

from ..models.enums.text_type import TextType


class LabelFactory:
    @classmethod
    def get_label_component(cls, text: str, label_type: TextType, align=Qt.AlignLeft,
                            set_underline: bool = False) -> QLabel:
        label = QLabel()
        label.setText(text)
        font = QFont('Times', label_type.value)
        font.setUnderline(set_underline)
        label.setFont(font)
        label.setAlignment(align)
        return label

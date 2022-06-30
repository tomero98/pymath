import os
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QLabel

from ..models.enums.text_type import TextType


class LabelFactory:
    @classmethod
    def get_label_component(cls, text: str, label_type: TextType, align=Qt.AlignLeft,
                            set_underline: bool = False, fixed_width: int = None,
                            need_word_wrap: bool = False, set_cursive: bool = False, set_bold: bool = False) -> QLabel:
        font = QFont('Times', label_type.value)
        font.setItalic(set_cursive)
        font.setBold(set_bold)
        font.setUnderline(set_underline)

        label = QLabel()
        label.setText(text)
        label.setFont(font)
        label.setAlignment(align)
        label.setWordWrap(need_word_wrap)

        if fixed_width:
            label.setFixedWidth(fixed_width)
        return label

    @classmethod
    def get_label_image_component(cls, image_name: str, width: int, height: int, align=Qt.AlignLeft) -> QLabel:
        image_path = cls._get_image_path(image_name=image_name)
        pixmap = QPixmap()
        pixmap.load(image_path)
        pixmap = pixmap.scaled(width, height, Qt.KeepAspectRatio)

        label = QLabel()
        label.setPixmap(pixmap)
        return label

    @staticmethod
    def _get_image_path(image_name: str) -> str:
        image_path = str(Path(os.path.dirname(os.path.abspath(__file__))).parent.parent.joinpath(f'media/{image_name}'))
        return image_path

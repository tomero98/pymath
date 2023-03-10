from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtWidgets import QPushButton, QSizePolicy


class ButtonFactory:
    @classmethod
    def get_button_component(cls, title: str, function_to_connect=None, is_disable: bool = False,
                             size_policy=(QSizePolicy.Fixed, QSizePolicy.Fixed), icon: QIcon = None,
                             icon_size: int = None, tooltip: str = '', minimum_width: int = None,
                             minimum_height: int = None, text_size: int = None) -> QPushButton:
        button = QPushButton(title)
        button.setSizePolicy(*size_policy)
        button.pressed.connect(function_to_connect)
        button.setDisabled(is_disable)
        button.setCursor(QCursor(Qt.PointingHandCursor))
        button.setToolTip(tooltip)

        if minimum_width:
            button.setMinimumWidth(minimum_width)

        if minimum_height:
            button.setMinimumHeight(minimum_height)

        if icon:
            button.setLayoutDirection(Qt.RightToLeft)
            button.setIcon(icon)
            button.setIconSize(QSize(icon_size, icon_size))
            button.setStyleSheet('border-radius: 25px')

        if text_size:
            button.setStyleSheet(f'font-size: {text_size}px')
        return button
